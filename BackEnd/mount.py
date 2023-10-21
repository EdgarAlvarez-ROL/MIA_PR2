import os
import sys
import time
import random
from structs import *
import struct
from mkdisk import MkDisk
from fdisk2 import *
from rmdisk import RmDisk

class Scanner:
    def __init__(self):
        pass

    @staticmethod
    def mayusculas(a):
        return a.upper()

    @staticmethod
    def comparar(a, b):
        return a.upper() == b.upper()
 
    @staticmethod
    def confirmar(mensaje):
        respuesta = input(f"{mensaje} (y/n)\n\t").lower()
        return respuesta == "y"

    def comando(self, text):
        tkn = ""
        terminar = False
        for c in text:
            if terminar:
                if c == ' ' or c == '-':
                    break
                tkn += c
            elif c != ' ' and not terminar:
                if c == '#':
                    tkn = text
                    break
                else:
                    tkn += c
                    terminar = True
        return tkn

    def separar_tokens(self, text):
        tokens = []
        if not text:
            return tokens
        text += ' '
        token = ""
        estado = 0
        for c in text:
            if estado == 0 and c == '-':
                estado = 1
            elif estado == 0 and c == '#':
                continue
            elif estado != 0:
                if estado == 1:
                    if c == '=':
                        estado = 2
                    elif c == ' ':
                        continue
                elif estado == 2:
                    if c == '\"':
                        estado = 3
                        continue
                    else:
                        estado = 4
                elif estado == 3:
                    if c == '\"':
                        estado = 4
                        continue
                elif estado == 4 and c == '\"':
                    tokens.clear()
                    continue
                elif estado == 4 and c == ' ':
                    estado = 0
                    tokens.append(token)
                    token = ""
                    continue
                token += c
        return tokens

class Mount:
    def __init__(self):
        self.alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.discoMontado = []   
        for _ in range(99): 
            tmp = DiscoMontado()
            self.discoMontado.append(tmp) 

    def retornoNombredelDisco(self, path):
        nombre_archivo = os.path.basename(path)
        # Imprime el nombre del archivo
        # print("El nombre del archivo es:", nombre_archivo)
        return nombre_archivo[:-4]

    def salida_consola(self,texto):
        try:
            with open("BackEnd\contenidoTXT\salida_consola.txt","a") as archivo:
                    archivo.write(texto)
        except Exception as e: 
            print(str(e))

    def validarDatos(self, context): 
        if not context:
            self.listaMount()
            return
        required = ["name", "path"]
        path = ""
        name = ""

        for current in context:
            id = current.split('=')[0]
            current = current.split('=')[1]
            if current[0] == "\"":
                current = current[1:-1]

            if Scanner.comparar(id, "name"):
                if id in required:
                    required.remove(id)
                    name = current
            elif Scanner.comparar(id, "path"):
                if id in required:
                    required.remove(id)
                    path = current

        if required:
            print("MOUNT", "requiere ciertos parámetros obligatorios")
            self.salida_consola("Mount requiere ciertos parametros\n")
            return
        self.mount(path, name)
    
   
 
    def mount(self, p, n):
        try:
            if not os.path.exists(p):
                self.salida_consola("Disco No existente\n")
                raise RuntimeError("disco no existente")

            namePart = self.retornoNombredelDisco(p)
              
            disk = MBR()  # Replace with actual initialization
            try: 
                with open(p, "rb") as file:
                    mbr_data = file.read()
                    disk.mbr_tamano = struct.unpack("<i", mbr_data[:4])[0]
                    disk.mbr_fecha_creacion = struct.unpack("<i", mbr_data[4:8])[0]
                    disk.mbr_disk_signature = struct.unpack("<i", mbr_data[8:12])[0]
                    disk.disk_fit = mbr_data[12:14].decode('utf-8')

                    partition_size = struct.calcsize("<iii16s")
                    partition_data = mbr_data[14:14 + partition_size]
                    disk.mbr_Partition_1.__setstate__(partition_data)
                     
                    partition_data = mbr_data[13 + partition_size:14 + 2 * partition_size]
                    disk.mbr_Partition_2.__setstate__(partition_data)
                    
                    partition_data = mbr_data[12 + 2 * partition_size:14 + 3 * partition_size]
                    disk.mbr_Partition_3.__setstate__(partition_data)
                    
                    partition_data = mbr_data[11 + 3 * partition_size:14 + 4 * partition_size]
                    disk.mbr_Partition_4.__setstate__(partition_data)

            except Exception as e:
                self.salida_consola(str(e)+"\n")
                print(e)
            partition = FDisk.buscarParticiones(self, disk, n, p)
            # partition = fdibuscarParticiones(disk, n, p) 
            if partition.part_type == 'E':
                if partition.part_name == n:
                    self.salida_consola("No se puede montar una particicon extendida\n")
                    raise RuntimeError("no se puede montar una partición extendida")
                else:
                    ebrs = FDisk.get_logicas(partition, p)
                    if ebrs:
                        for ebr in ebrs:
                            if ebr.part_name == n and ebr.part_status == '1':
                                n = ebr.part_name

            
            for i in range(99):
                if self.discoMontado[i].path == p:
                    for j in range(26):
                        if self.discoMontado[i].particiones[j].estado == '0':
                            self.discoMontado[i].particiones[j].estado = '1'
                            self.discoMontado[i].particiones[j].letra = namePart
                            self.discoMontado[i].particiones[j].nombre = n
                            re = "44" + str(i + 1) + namePart #self.alfabeto[j]
                            print(re)
                            print("MOUNT", "se ha realizado correctamente el mount -id=: " + re)
                            self.salida_consola(f"Mount se ha realizado correctamente el mound del -id={re} \n")
                            return
                        

            for i in range(99):
                if self.discoMontado[i].estado == '0':
                    self.discoMontado[i].estado = '1'
                    self.discoMontado[i].path = p
                    for j in range(26):
                        if self.discoMontado[i].particiones[j].estado == '0':
                            self.discoMontado[i].particiones[j].estado = '1'
                            self.discoMontado[i].particiones[j].letra = namePart
                            self.discoMontado[i].particiones[j].nombre = n
                            re = "44" + str(i + 1) + namePart    #self.alfabeto[j]

                            #Para mí era los ID'S se calculaban de la siguiente manera: *Últimos dos dígitos del Carnet + Número + Letra Ejemplo: carnet = 201404106
                            #Id ́s = 061A, 061B, 061C, 062A, 063A

                            # YO LO CAMBIE ENVEZ DE LETRA NOMBRE ENVIADO
                            # print(re)
                            print("MOUNT", "se ha realizado correctamente el mount -id=" + re)
                            self.salida_consola(f"Mount se ha realizado correctamente el mount del -id={re} \n")
                            return
        except Exception as e:
            self.salida_consola(f"Mount {e} \n")
            print("MOUNT", e)
 
    def validarDatosU(self, context):
        required = ["id"]
        id_ = ""

        for current in context:
            id = current.split('=')[0]
            current = current.split('=')[1]

            if Scanner.comparar(id, "id"):
                if id in required:
                    required.remove(id)
                    id_ = current

        if required:
            print("UNMOUNT", "requiere ciertos parámetros obligatorios")
            self.salida_consola("UNMOUNT requiere ciertos parametros\n")
            return
        self.unmount(id_)
 
    def getmount(self, id, p):
        if not (id[0] == '4' and id[1] == '4'):
            self.salida_consola("el primer identificador no es válido \n")
            raise RuntimeError("el primer identificador no es válido")
        past = id
        letter = id[3:]
        id = id[2:3]
        i = int(id) - 1
        if i < 0:
            self.salida_consola("identificador de disco inválido\n")
            raise RuntimeError("identificador de disco inválido")

        # print(letter, id, i)

        for j in range(26):
            if self.discoMontado[i].particiones[j].estado == '1':
                if self.discoMontado[i].particiones[j].letra == letter:
                    # print("entramos : "+ letter)
                    if not os.path.exists(self.discoMontado[i].path):
                        self.salida_consola("MOUNT Disco no existente\n")
                        raise RuntimeError("disco no existente")

                    disk = MBR()  # Replace with actual initialization
                    # with open(self.discoMontado[i].path, "rb") as validate:
                        # validate.seek(0)
                        # validate.readinto(disk)

                        #  ================================================
                    try:
                        with open(self.discoMontado[i].path, "rb") as validate:
                            mbr_data = validate.read()
                            # if len(mbr_data) != MBR.SIZE:  # Make sure the read data has the expected size
                            #     raise RuntimeError("Invalid MBR data size")
                            # Unpack the MBR data into the disk object
                            disk.mbr_tamano = struct.unpack("<i", mbr_data[:4])[0]
                            disk.mbr_fecha_creacion = struct.unpack("<i", mbr_data[4:8])[0]
                            disk.mbr_disk_signature = struct.unpack("<i", mbr_data[8:12])[0]
                            disk.disk_fit = mbr_data[12:14].decode('utf-8')
                            # Unpack each partition
                            partition_size = struct.calcsize("<iii16s")
                            partition_data = mbr_data[14:14 + partition_size]
                            disk.mbr_Partition_1.__setstate__(partition_data)
                            partition_data = mbr_data[14 + partition_size:14 + 2 * partition_size]
                            disk.mbr_Partition_2.__setstate__(partition_data)
                            partition_data = mbr_data[14 + 2 * partition_size:14 + 3 * partition_size]
                            disk.mbr_Partition_3.__setstate__(partition_data)
                            partition_data = mbr_data[14 + 3 * partition_size:14 + 4 * partition_size]
                            disk.mbr_Partition_4.__setstate__(partition_data)
                    except Exception as e:
                        self.salida_consola(f"Error reading and unpacking MBR data from the disk file: {str(e)} \n")
                        raise RuntimeError("Error reading and unpacking MBR data from the disk file: " + str(e))

                        #  ================================================

                    
                    p = self.discoMontado[i].path
                    # print(self.discoMontado[i].particiones[j].nombre)
                    return FDisk.buscarParticiones(self, disk, self.discoMontado[i].particiones[j].nombre, self.discoMontado[i].path), p
        self.salida_consola("particion no existente \n")
        raise RuntimeError("partición no existente")
 
    def listaMount(self):
        print("\n<-------------------------- LISTADO DE MOUNTS -------------------------->")
        self.salida_consola("\n<-------------------------- LISTADO DE MOUNTS -------------------------->\n")
        for i in range(99):
            for j in range(26):
                namePart = self.discoMontado[i].particiones[j].letra
                if namePart != "":
                    print(namePart)
                    self.salida_consola(str(namePart))
                if self.discoMontado[i].particiones[j].estado == '1':
                    print("> 87" + str(i + 1) + " : " + namePart + ", " + self.discoMontado[i].particiones[j].nombre)
                    self.salida_consola("> 87" + str(i + 1) + " : " + namePart + ", " + self.discoMontado[i].particiones[j].nombre)
        print("\n")
        self.salida_consola("\n")

    def unmount(self, id):
        try:
            if not (id[0] == '4' and id[1] == '4'):
                self.salida_consola("el primer identificador no es válido\n")
                raise RuntimeError("el primer identificador no es válido")
            past = id
            letter = id[3:]
            
            # i = int(id) - 1
            i = int(id[2]) - 1
            if i < 0:
                self.salida_consola("identificador de disco inválido\n")
                raise RuntimeError("identificador de disco inválido")
            # print(letter) # tiene que ser el nombre del disco nada mas asi se instancio arriba
            for j in range(26):
                if self.discoMontado[i].particiones[j].estado == '1':
                    if self.discoMontado[i].particiones[j].letra == letter:
                        mp = ParticionMontada()
                        self.discoMontado[i].particiones[j] = mp
                        print("UNMOUNT", "se ha realizado correctamente el unmount -id=" + past)
                        self.salida_consola(f"UNMOUNT se ha realizado correctamente el unmoun del -id={past} \n")
                        return
            self.salida_consola(f"No se encontró el -id={id} no se desmontó nada\n")
            raise RuntimeError("No se encontró el -id= " + id + ", no se desmontó nada")
        except ValueError:
            self.salida_consola("UNMOUNT identificador de disco incorrecto, debe ser entero\n")
            print("UNMOUNT", "identificador de disco incorrecto, debe ser entero")
        except Exception as e:
            self.salida_consola(f"UNMOUNT {e}\n")
            print("UNMOUNT", e)
 
