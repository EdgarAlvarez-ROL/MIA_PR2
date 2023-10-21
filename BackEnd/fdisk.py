from structs import Particion, MBR, Transition, EBR
import os
import sys
import random
import time
import struct

# startValue

class FDisk:
    def __init__(self):
        self.size= 0
        self.fit = ''
        self.unit = ''
        self.path = ''
        self.name = ''
        self.type = ''
        self.delete = '' #FULL para borrar todo
        self.add = 0

    def recibeData(self):
        # print(self.path)
        eliminar = False
        if self.delete == "FULL":
            print(self.delete)
            eliminar = True
        # falta otra cosa que no se
        # print(eliminar)
        if not eliminar:
            required = ["size", "path", "name"]
            size = 0
            unit = "K"
            path = ""
            type = "P"
            fit = "WF"
            add = 0
            name = ""
            if int(self.size) > 0:
                size = int(self.size)
                required.remove("size")
            else:
                print("\tERROR: El valor del Size es negativo o 0") 
                return
            
            if os.path.exists(self.path):
                required.remove("path")
                if self.path.startswith("\""):
                    self.path = self.path[1:-1]
                if not self.path.endswith(".dsk"):
                    print("\tERROR: Extensión de archivo no válida para la creación del Disco.")
                    return
                path = self.path
                # print("path path ")
                # print(path)
            else:
                print("\tERROR: Disco no Existente en la ruta indicada") 
                return
            
            if self.name != "":
                name = self.name
                required.remove("name")
            
            # if self.unit == "M":
            #     size = 1024 * 1024 * size
            #     unit = self.unit
            # elif self.unit == "B":
            #     unit = self.unit
            # elif self.unit == "K":
            #     size = 1024 * size    
            #     unit = self.unit
            else: 
                print("\tERROR: Unit indicado no aceptado") 
                return           
            
            if self.type == "P":
                type = "P"
            elif self.type == "E":
                type = "E"
            elif self.type == "L":
                type = "L"
            else: 
                print("\tERROR: Type indicado no aceptado") 
                return

            fit = self.fit
            unit = self.unit

            if required:
                print("\tERROR: Faltan parámetros obligatorios para el comando FDISK") 
                return
            if self.add == 0:
                # print(path)
                print(size)
                print(unit)
                print(path)
                print(type)
                print(fit )
                print(add )
                print(name)
                print("")
                self.generarParticion(size, unit, path, type, fit, name, add)
            else:
                print("SE AGREGARA ESPACIO A LA PARTICION")
                #agregarParticion(add, unit, name, path)
        
        # Si eliminar es TRUE
        else:
            print("ENTROMS ELIMINAR")
            required = ["path", "name"]
            path = ""
            name = ""
            if os.path.exists(self.path):
                required.remove("path")
                if self.path.startswith("\"") and self.path.endswith("\""):
                    self.path = self.path[1:-1]
                    path = self.path
                if not self.path.endswith(".dsk"):
                    print("\tERROR: Extensión de archivo no válida para la creación del Disco.")
                    return
            else:
                print("\tERROR: Disco no Existente en la ruta indicada") 
                return
            
            if self.name != "":
                name = self.name
                required.remove("name")
            else:
                print("\tERROR: Nombre de la particion no ingresada") 
                return
            
            if required:
                print("\tERROR: Faltan parámetros obligatorios para el comando FDISK junto con el parámetro DELETE") 
                return
            else:
                print("SE ELIMINARA LA PARTICION")
                confirmacion = input("\t---- Esta seguro que desea eliminar la particion Y/N: ")
                if confirmacion == 'Y' or confirmacion == 'y' or confirmacion == '1':
                        #eliminarParticion(elimi, path, name)
                        print(f"\t==== PARTICION {name} eliminada correctamente ====")
                else:
                        print(f"\t==== La Particion {name} no se borro [no se preocupe, todo bien ;) ] ====")
            

# logica
    def logica(self, partition, ep, p):
        nlogic = EBR()
        nlogic.part_status = '1'
        nlogic.part_fit = partition.part_fit
        nlogic.part_size = partition.part_size
        nlogic.part_next = -1
        nlogic.part_name = partition.part_name

        with open(p, "rb+") as file:
            file.seek(0)
            tmp = EBR()
            file.seek(ep.part_start -1)
            tmp_data = file.read(struct.calcsize("c2s3i3i16s"))
            tmp.__setstate__(tmp_data)
            size = 0
            while True:
                size += struct.calcsize("c2s3i3i16s") + tmp.part_size
                if (tmp.part_status == '0' or tmp.part_status == '\x00') and tmp.part_next == -1:
                    nlogic.part_start = tmp.part_start
                    nlogic.part_next = nlogic.part_start + nlogic.part_size + struct.calcsize("c2s3i3i16s")
                    if (ep.part_size - size) <= nlogic.part_size:
                        raise RuntimeError("no hay espacio para más particiones lógicas")
                    file.seek(nlogic.part_start-1) 
                    file.write(nlogic.__bytes__())
                    file.seek(nlogic.part_next)
                    addLogic = EBR()
                    addLogic.part_status = '0'
                    addLogic.part_next = -1
                    addLogic.part_start = nlogic.part_next
                    file.seek(addLogic.part_start)
                    file.write(addLogic.__bytes__())
                    name = nlogic.part_name
                    print(f"partición lógica: {name}, creada correctamente.")
                    return
                file.seek(tmp.part_next-1)
                tmp_data = file.read(struct.calcsize("c2s3i3i16s"))
                tmp.__setstate__(tmp_data)

    # update
    def update_start_value(self, new_value):
        global startValue
        startValue = new_value

    # ajustar
    def ajustar(self,mbr, p, t, ps, u):
        if u == 0:
            p.part_start = sys.getsizeof(mbr)
            startValue = p.part_start
            self.update_start_value(p.part_start)
            mbr.mbr_Partition_1 = p
            return mbr
        else:
            usar = Transition()
            c = 0
            for tr in t:
                if c == 0:
                    usar = tr
                    c += 1
                    continue

                if mbr.disk_fit[0].upper() == 'F':
                    if usar.before >= p.part_size or usar.after >= p.part_size:
                        break
                    usar = tr
                elif mbr.disk_fit[0].upper() == 'B':
                    if usar.before < p.part_size or usar.after < p.part_size:
                        usar = tr
                    else:
                        if tr.before >= p.part_size or tr.after >= p.part_size:
                            b1 = usar.before - p.part_size
                            a1 = usar.after - p.part_size
                            b2 = tr.before - p.part_size
                            a2 = tr.after - p.part_size

                            if (b1 < b2 and b1 < a2) or (a1 < b2 and a1 < a2):
                                c += 1
                                continue
                            usar = tr
                elif mbr.disk_fit[0].upper() == 'W':
                    if usar.before < p.part_size or usar.after < p.part_size:
                        usar = tr
                    else:
                        if tr.before >= p.part_size or tr.after >= p.part_size:
                            b1 = usar.before - p.part_size
                            a1 = usar.after - p.part_size
                            b2 = tr.before - p.part_size
                            a2 = tr.after - p.part_size
                            if (b1 > b2 and b1 > a2) or (a1 > b2 and a1 > a2):
                                c += 1
                                continue
                            usar = tr
                c += 1

            if usar.before >= p.part_size or usar.after >= p.part_size:
                if mbr.disk_fit[0].upper() == 'F':
                    if usar.before >= p.part_size:
                        p.part_start = (usar.start - usar.before)
                        startValue = p.part_start
                        self.update_start_value(p.part_start)
                    else:
                        p.part_start = usar.end
                        startValue = p.part_start
                        self.update_start_value(p.part_start)
                elif mbr.disk_fit[0].upper() == 'B':
                    b1 = usar.before - p.part_size
                    a1 = usar.after - p.part_size

                    if (usar.before >= p.part_size and b1 < a1) or usar.after < p.part_start:
                        p.part_start = (usar.start - usar.before)
                        startValue = p.part_start
                        self.update_start_value(p.part_start)
                    else:
                        p.part_start = usar.end
                        startValue = p.part_start
                        self.update_start_value(p.part_start)
                elif mbr.disk_fit[0].upper() == 'W':
                    b1 = usar.before - p.part_size
                    a1 = usar.after - p.part_size

                    if (usar.before >= p.part_size and b1 > a1) or usar.after < p.part_start:
                        p.part_start = (usar.start - usar.before)
                        startValue = p.part_start
                        self.update_start_value(p.part_start)
                    else:
                        p.part_start = usar.end
                        startValue = p.part_start
                        self.update_start_value(p.part_start)

                partitions = [Particion() for _ in range(4)]

                for i in range(len(ps)):
                    partitions[i] = ps[i]
                
                for i in range(len(partitions)):
                    if partitions[i].part_status == '0':
                        partitions[i] = p
                        break
                mbr.mbr_Partition_1 = partitions[0]
                mbr.mbr_Partition_2 = partitions[1]
                mbr.mbr_Partition_3 = partitions[2]
                mbr.mbr_Partition_4 = partitions[3]
                return mbr
            else:
                raise RuntimeError("no hay espacio suficiente")

# ajustar

    def generarParticion(self, s, u, p, t, f, n, a):
        try:
            i = int(s)
            if i <= 0:
                raise RuntimeError("-size debe de ser mayor que 0")
            
            # if u.lower() in ["b", "k", "m"]:
            #     if u.lower() != "b":
            #         if u.lower() == "k":
            #             i *= 1024
            #         else:
            #             i *= 1024 * 1024
            else:
                raise RuntimeError("-unit no contiene los valores esperados...")
            
            if p[:1] == "\"":
                p = p[1:-1]
            
            if t.lower() not in ["p", "e", "l"]:
                raise RuntimeError("-type no contiene los valores esperados...")
            
            if f.lower() not in ["bf", "ff", "wf"]:
                raise RuntimeError("-fit no contiene los valores esperados...")
            
            try:
                mbr = MBR()
                with open(p, "rb") as file:
                    mbr_data = file.read()
                    mbr.mbr_tamano = struct.unpack("<i", mbr_data[:4])[0]
                    mbr.mbr_fecha_creacion = struct.unpack("<i", mbr_data[4:8])[0]
                    mbr.mbr_disk_signature = struct.unpack("<i", mbr_data[8:12])[0]
                    mbr.disk_fit = mbr_data[12:14].decode('utf-8')

                    partition_size = struct.calcsize("<iii16s")
                    partition_data = mbr_data[14:14 + partition_size]
                    mbr.mbr_Partition_1.__setstate__(partition_data)
                     
                    partition_data = mbr_data[13 + partition_size:14 + 2 * partition_size]
                    mbr.mbr_Partition_2.__setstate__(partition_data)
                    
                    partition_data = mbr_data[12 + 2 * partition_size:14 + 3 * partition_size]
                    mbr.mbr_Partition_3.__setstate__(partition_data)
                    
                    partition_data = mbr_data[11 + 3 * partition_size:14 + 4 * partition_size]
                    mbr.mbr_Partition_4.__setstate__(partition_data)

            except Exception as e:
                print(e)

            
            partitions = [mbr.mbr_Partition_1, mbr.mbr_Partition_2, mbr.mbr_Partition_3, mbr.mbr_Partition_4]
            between = []
            used = 0
            ext = 0
            c = 1
            base = sys.getsizeof(mbr) 
            extended = Particion()
            for prttn in partitions:
                if prttn.part_status == '1':
                    trn = Transition()
                    trn.partition = c
                    trn.start = prttn.part_start
                    trn.end = prttn.part_start + prttn.part_size
                    trn.before = trn.start - base
                    base = trn.end
                    if used != 0:
                        between[used - 1].after = trn.start - (between[used - 1].end)
                    between.append(trn)
                    used += 1

                    if prttn.part_type.lower() == 'e':
                        ext += 1
                        extended = prttn
                else: 
                    partitions[c - 1] = Particion()

                if used == 4 and t.lower() != "l":
                    raise RuntimeError("Limite de particiones alcanzado")
                elif ext == 1 and t.lower() == "e":
                    raise RuntimeError("Solo se puede crear una particion Extendida.")

                mbr.mbr_Partition_1 = partitions[0]
                mbr.mbr_Partition_2 = partitions[1]
                mbr.mbr_Partition_3 = partitions[2]
                mbr.mbr_Partition_4 = partitions[3]
                
                c += 1
            
            if ext == 0 and t.lower() == "l":
                raise RuntimeError("No existe particion Extendida para crear la Logica")
            
            if used != 0:
                between[-1].after = mbr.mbr_tamano - between[-1].end
            
            try:
                self.buscarParticiones(mbr, n, p)
                print("FDISK", "El nombre: "+n+" ya existe en el disco")
                return
            except Exception as e:
                print(e)
            
            temporal = Particion()
            temporal.part_status = '1'
            temporal.part_size = i
            temporal.part_type = t[0].upper()
            temporal.part_fit = f[0].upper()
            temporal.part_name = n
            
            if t.lower() == "l": 
                self.logica(temporal, extended, p)
                return
            
            mbr = self.ajustar(mbr, temporal, between, partitions, used)
            with open(p, "rb+") as bfile:
                bfile.write(mbr.__bytes__())
                if t.lower() == "e":
                    ebr = EBR()
                    ebr.part_start = startValue 
                    bfile.seek(startValue, 0)
                    bfile.write(ebr.__bytes__())
                    print("FDISK", "partición extendida:", n, "creada correctamente")
                    return
                print("FDISK", "partición primaria:", n, "creada correctamente")
        except ValueError as e: 
            print("FDISK", "-size debe ser un entero")
        except Exception as e: 
            print("FDISK", str(e))
   

    def get_logicas(self, partition, p):
        ebrs = []

        with open(p, "rb+") as file:
            start_position = partition.part_start -1
            if start_position < 0:
                start_position = 0
                
            file.seek(start_position, 0)
            tmp_data = file.read(struct.calcsize("c2s3i3i16s"))

            while len(tmp_data) == struct.calcsize("c2s3i3i16s"):
                tmp = EBR()
                tmp.__setstate__(tmp_data)
                if tmp.part_next != -1 :
                    ebrs.append(tmp)
                    file.seek(tmp.part_next-1, 0)
                    tmp_data = file.read(struct.calcsize("c2s3i3i16s"))
                else:
                    break

        return ebrs



    def buscarParticiones(self, mbr, name, path):
            partitions = [mbr.mbr_Partition_1, mbr.mbr_Partition_2, mbr.mbr_Partition_3, mbr.mbr_Partition_4]
            ext = False
            extended = Particion()

            for partition in partitions:
                if partition.part_status == '1':
                    if partition.part_name == name:
                        return partition
                    elif partition.part_type == 'E':
                        ext = True
                        extended = partition

            if ext:
                ebrs = self.get_logicas(extended, path)
                for ebr in ebrs:
                    if ebr.part_status == '1':
                        if ebr.part_name == name:
                            tmp = Particion()
                            tmp.part_status = '1'
                            tmp.part_type = 'L'
                            tmp.part_fit = ebr.part_fit
                            tmp.part_start = ebr.part_start
                            tmp.part_size = ebr.part_size
                            tmp.part_name = ebr.part_name
                            return tmp
            raise RuntimeError("Creando la partición: " + name + "...")

