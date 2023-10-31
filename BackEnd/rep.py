from structs import MBR, Particion, EBR, SuperBloque
import struct
import structs
import pickle
import mount as Mount
import fdisk2
import datetime
import time
import graficas


class reporte:
    def __init__(self):
        self.path = ''

    def repMBR(self):
        if self.path:
            if self.path.startswith("\"") and self.path.endswith("\""):
                self.path = self.path[1:-1]
        dot = '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'''
        try: 
            mbr_format = "<iiiiB"
            mbr_size = struct.calcsize(mbr_format)

            # partition_format = "c2s3i3i16s"
            partition_format = "c2s3i3i16s"
            partition_size = struct.calcsize(partition_format)
            # print(particion_size)
            tamanioSuperBloque = struct.calcsize("<iiiiiddiiiiiiiiii")
            data = ""
            with open(self.path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                # print(particion_data)
                mbr = MBR()
                (mbr.mbr_tamano, mbr.mbr_fecha_creacion, mbr.mbr_disk_signature, disk_fit, mbr.mbr_Partition_1, *_) = struct.unpack(mbr_format, mbr_data)
                mbr.disk_fit = chr(disk_fit % 128) 

                
                partition1 = Particion()
                particion_data = b'1PW'+ particion_data
                particion_data = particion_data[:-2]
                # print("PARTICON DATA")
                # print(particion_data)
                partition1.__setstate__(particion_data)
                

                """==================================="""
                # print("============================")
                # print(superBloque_data)
                super_Bloque = SuperBloque()
                
                # print(len(superBloque_data))
                # data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
                # print(superBloque_data)
                # print("============================")
                """==================================="""
                # lo que deberia
                # b'\x02\x00\x00\x00)7\x00\x00{\xa5\x00\x00{\xa5\x00\x00)7\x00\x00\x00\x00@\xd2\xfb>\xd9A\x00\x00@\xd2\xfb>\xd9A\x01\x00\x00\x00S\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\xad7\x00\x00(\xdd\x00\x00\xb1\xc3\x15\x00'
                # b'                  \x00\x00{\xa5\x00\x00{\xa5\x00\x00)7\x00\x00\x00\x00@\xd2\xfb>\xd9A\x00\x00@\xd2\xfb>\xd9A\x01\x00\x00\x00S\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\xad7\x00\x00(\xdd\x00\x00\xb1\xc3\x15\x00\x0011000'
                # lo que salio

                # if superBloque_data == b'\x02\x00\x00\x00)7\x00\x00{\xa5\x00\x00{\xa5\x00\x00)7\x00\x00\x00\x00@\xd2\xfb>\xd9A\x00\x00@\xd2\xfb>\xd9A\x01\x00\x00\x00S\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\xad7\x00\x00(\xdd\x00\x00\xb1\xc3\x15\x00':
                    # print("chupala")

                # Data es la info del superbloque
                # print("###########################")
                # b'\x01\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x98\x02\x00\x00'
                # b'\x01\x00\x00\x00\x01\x00\x00\x00[\x00\x00\x00\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x01\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x98\x02\x00\x00'
                # print("###########################")
                # 
                file.close()
        except Exception as e:
            print("\tERROR: No se pudo leer el disco en la ruta: " + self.path+", debido a: "+str(e))


           

        print("\t============ MBR \t============")
        print("\tMBR tamaño:", mbr.mbr_tamano)
        print("\tMBR fecha creación:", mbr.mbr_fecha_creacion)
        print("\tDisco fit:", mbr.disk_fit)
        print("\tMBR disk signature:", mbr.mbr_disk_signature)

        fecha_y_hora = datetime.datetime.utcfromtimestamp(mbr.mbr_fecha_creacion)

        # Formatear la fecha y hora según tus preferencias
        formato = "%Y-%m-%d %H:%M:%S"  # Puedes ajustar el formato como desees
        fecha_formateada = fecha_y_hora.strftime(formato)
        dot += f'''  <TR>
                        <TD colspan="2">REPORTE MBR</TD>
                        
                    </TR>
                    <TR>
                        <TD>mbr_tamaño:</TD>
                        <TD>{mbr.mbr_tamano}</TD>
                    </TR>
                    <TR>
                        <TD>mbr_fecha_creacion:</TD>
                        <TD>{fecha_formateada}</TD>
                    </TR>
                    <TR>
                        <TD>mbr_disk_signature:</TD>
                        <TD>{mbr.mbr_disk_signature}</TD>
                    </TR>
                    '''
        # print(dot)
        print("\t============ PARTICION ===========")
        print("\tMBR Particion Status: ", partition1.part_status)
        print("\tMBR Particion TYpe: ", partition1.part_type)
        print("\tMBR Particion FIt: ", partition1.part_fit)
        print("\tMBR Particion Start: ", partition1.part_start)
        print("\tMBR Particion SIze: ", partition1.part_size)
        print("\tMBR Particion Name: ", partition1.part_name)
        
        #if partition1.part_name[0].isdigit():
 #           partition1.part_name = ""

        dot += f'''
                    <TR>
                        <TD>PARTICION</TD>
                        <TD>    </TD>
                    </TR>
                    <TR>
                        <TD>part_status:</TD>
                        <TD>{partition1.part_status}</TD>
                    </TR>
                    <TR>
                        <TD>part_type</TD>
                        <TD>{partition1.part_type}</TD>
                    </TR>
                    <TR>
                        <TD>part_fit</TD>
                        <TD>{partition1.part_fit}</TD>
                    </TR>
                    <TR>
                        <TD>part_start</TD>
                        <TD>{partition1.part_start}</TD>
                    </TR>
                    <TR>
                        <TD>part_size</TD>
                        <TD>{partition1.part_size}</TD>
                    </TR>
                    <TR>
                        <TD>part_name</TD>
                        <TD>{partition1.part_name}</TD>
                    </TR>

        '''


        
        

        info_E = self.obtenerParticonExtendida(partition1.part_size)
        part3 = self.obtenerParticion3(44+44)
        part4 = self.obtenerParticion3(44+44+44)
        dot += info_E + part3 + part4
        dot+= '''</TABLE>>'''
        
        # print(dot)
        graficas.rep_MBR(dot)


        # pp = data[15]
        # self.replicaa(pp)
        # print(data)
        
    def obtenerParticonExtendida(self, final_particion1):
        ''''''
        dot = ''
        try: 
            mbr_format = "<iiiiB"
            mbr_size = struct.calcsize(mbr_format)

            # partition_format = "c2s3i3i16s"
            partition_format = "c2s3i3i16s"
            partition_size = struct.calcsize(partition_format)
            
            # print(partition_size)


            partition1 = Particion()
            # print(particion_size)
            tamanioSuperBloque = struct.calcsize("<iiiiiddiiiiiiiiii")
            data = ""
            with open(self.path, "rb") as file:
                
                mbr_data = file.read(mbr_size)
                
                file.seek(44)
                particion_data = file.read(partition_size)
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                # print(particion_data)
                mbr = MBR()
                (mbr.mbr_tamano, mbr.mbr_fecha_creacion, mbr.mbr_disk_signature, disk_fit, mbr.mbr_Partition_1, *_) = struct.unpack(mbr_format, mbr_data)
                mbr.disk_fit = chr(disk_fit % 128) 

                # print(particion_data)
                
                particion_data = b'1EW'+ particion_data
                particion_data = particion_data[:-2]
                # print("PARTICON DATA")
                
                partition1.__setstate__(particion_data)
                # print(partition1.part_size)
                
        except Exception as e:
            print("\tERROR: No se pudo leer el disco en la ruta: " + self.path+", debido a: "+str(e))
        

        print("\t============ PARTICION EXTENDIDA ===========")
        print("\tMBR Particion Status: ", partition1.part_status)
        print("\tMBR Particion TYpe: ", partition1.part_type)
        print("\tMBR Particion FIt: ", partition1.part_fit)
        print("\tMBR Particion Start: ", partition1.part_start)
        print("\tMBR Particion SIze: ", partition1.part_size)
        print("\tMBR Particion Name: ", partition1.part_name)
        #if partition1.part_name[0].isdigit():
 #           partition1.part_name = ""
        dot += f'''
                    <TR>
                        <TD colspan="2">PARTICION</TD>
                        
                    </TR>
                    <TR>
                        <TD>part_status:</TD>
                        <TD>{partition1.part_status}</TD>
                    </TR>
                    <TR>
                        <TD>part_type</TD>
                        <TD>{partition1.part_type}</TD>
                    </TR>
                    <TR>
                        <TD>part_fit</TD>
                        <TD>{partition1.part_fit}</TD>
                    </TR>
                    <TR>
                        <TD>part_start</TD>
                        <TD>{partition1.part_start}</TD>
                    </TR>
                    <TR>
                        <TD>part_size</TD>
                        <TD>{partition1.part_size}</TD>
                    </TR>
                     <TR>
                        <TD>part_name</TD>
                        <TD>{str(partition1.part_name)}</TD>
                    </TR>

        '''


        return dot


    def obtenerParticion3(self, final_particion1):
        ''''''
        dot = ''
        try: 
            mbr_format = "<iiiiB"
            mbr_size = struct.calcsize(mbr_format)

            # partition_format = "c2s3i3i16s"
            partition_format = "c2s3i3i16s"
            partition_size = struct.calcsize(partition_format)
            
            # print(partition_size)


            partition1 = Particion()
            # print(particion_size)
            tamanioSuperBloque = struct.calcsize("<iiiiiddiiiiiiiiii")
            data = ""
            with open(self.path, "rb") as file:
                
                mbr_data = file.read(mbr_size)
                
                file.seek(final_particion1)
                particion_data = file.read(partition_size)
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                # print(particion_data)
                mbr = MBR()
                (mbr.mbr_tamano, mbr.mbr_fecha_creacion, mbr.mbr_disk_signature, disk_fit, mbr.mbr_Partition_1, *_) = struct.unpack(mbr_format, mbr_data)
                mbr.disk_fit = chr(disk_fit % 128) 

                # print(particion_data)
                
                particion_data = b'1LW'+ particion_data
                particion_data = particion_data[:-2]
                # print("PARTICON DATA")
                
                partition1.__setstate__(particion_data)
                # print(partition1.part_size)
                
        except Exception as e:
            print("\tERROR: No se pudo leer el disco en la ruta: " + self.path+", debido a: "+str(e))
        

        print("\t============ PARTICION ===========")
        print("\tMBR Particion Status: ", partition1.part_status)
        print("\tMBR Particion TYpe: ", partition1.part_type)
        print("\tMBR Particion FIt: ", partition1.part_fit)
        print("\tMBR Particion Start: ", partition1.part_start)
        print("\tMBR Particion SIze: ", partition1.part_size)
        print("\tMBR Particion Name: ", partition1.part_name)
        #if partition1.part_name[0].isdigit():
 #           partition1.part_name = ""
        dot += f'''
                    <TR>
                        <TD colspan="2">PARTICION</TD>
                    </TR>
                    <TR>
                        <TD>part_status:</TD>
                        <TD>{partition1.part_status}</TD>
                    </TR>
                    <TR>
                        <TD>part_type</TD>
                        <TD>{partition1.part_type}</TD>
                    </TR>
                    <TR>
                        <TD>part_fit</TD>
                        <TD>{partition1.part_fit}</TD>
                    </TR>
                    <TR>
                        <TD>part_start</TD>
                        <TD>{partition1.part_start}</TD>
                    </TR>
                    <TR>
                        <TD>part_size</TD>
                        <TD>{partition1.part_size}</TD>
                    </TR>
                     <TR>
                        <TD>part_name</TD>
                        <TD>{str(partition1.part_name)}</TD>
                    </TR>

        '''


        return dot


    def replicaa(self, p):
        try:
            inode = structs.Inodos()  # Crear una instancia de SuperBloque
            bytes_inodo= bytes(inode)  # Obtener los bytes de la instancia

            recuperado = bytearray(len(bytes_inodo))  # Crear un bytearray del mismo tamaño
            # print(recuperado)
            tamanoInodos = struct.calcsize("<iiiddd15ici") 

            with open(self.path, "rb") as archivo:
                archivo.seek(p)
                archivo.readinto(recuperado)
                # inodos_data = archivo.read(101)

            # print(recuperado)
            # Desempaquetar los datos del bytearray recuperado
            inode.i_uid   = struct.unpack("<i", recuperado[:4])[0]
            inode.i_gid   = struct.unpack("<i", recuperado[4:8])[0] 
            inode.i_size  = struct.unpack("<i", recuperado[8:12])[0]
            inode.i_atime = struct.unpack("<d", recuperado[12:20])[0]
            inode.i_ctime = struct.unpack("<d", recuperado[20:28])[0]
            inode.i_mtime = struct.unpack("<d", recuperado[28:36])[0]
            inode.i_block = struct.unpack("<15i", recuperado[36:96])
            inode.i_type  = struct.unpack("<c", recuperado[96:97])[0] #recuperado[28:32].decode('utf-8')
            inode.i_perm  = struct.unpack("<i", recuperado[97:101])[0]


            inodeTemp = structs.Inodos()            
            with open(self.path, "rb") as archivo:
                archivo.seek(p+len(recuperado))
                archivo.readinto(recuperado)

            inodeTemp.i_perm  = struct.unpack("<i", recuperado[97:101])[0]
            print(inodeTemp.i_perm)
            # print(recuperado)
            """<iiiddd15ici"""
            # print(inode.i_uid  )
            # print(inode.i_gid  )
            # print(inode.i_size )
            # print(inode.i_atime)
            # print(inode.i_ctime)
            # print(inode.i_mtime)
            # print(inode.i_block)
            # print(inode.i_type )
            # print(inode.i_perm )
            
        except Exception as e:
            print(e)



    def repFDISK2(self, final_part):
        total = 0
        tamano_MBR = 0
        if final_part != 0:
            try: 
                mbr_format = "<iiiiB"
                mbr_size = struct.calcsize(mbr_format)

                # partition_format = "c2s3i3i16s"
                partition_format = "c2s3i3i16s"
                partition_size = struct.calcsize(partition_format)
                # print(particion_size)
                tamanioSuperBloque = struct.calcsize("<iiiiiddiiiiiiiiii")
                data = ""
                with open(self.path, "rb") as file:

                    mbr_data = file.read(mbr_size)

                    file.seek(final_part)
                    particion_data = file.read(partition_size)
                    superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                    # print(particion_data)
                    mbr = MBR()
                    (mbr.mbr_tamano, mbr.mbr_fecha_creacion, mbr.mbr_disk_signature, disk_fit, mbr.mbr_Partition_1, *_) = struct.unpack(mbr_format, mbr_data)
                    mbr.disk_fit = chr(disk_fit % 128) 


                    partition1 = Particion()
                    particion_data = b'1PW'+ particion_data
                    particion_data = particion_data[:-2]
                    # print("PARTICON DATA")
                    # print(particion_data)
                    partition1.__setstate__(particion_data)

                    total = int(partition1.part_size)
                    tamano_MBR = mbr.mbr_tamano
                    """==================================="""
                    # print("============================")
                    # print(superBloque_data)
                    super_Bloque = SuperBloque()

                    # print(len(superBloque_data))
                    # data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
                    superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                    superBloque_data = superBloque_data[:-6]
                    # print(superBloque_data)
                    data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
                    # print(superBloque_data)
                    # print("============================")
                    """==================================="""
                    # lo que deberia
                    # b'\x02\x00\x00\x00)7\x00\x00{\xa5\x00\x00{\xa5\x00\x00)7\x00\x00\x00\x00@\xd2\xfb>\xd9A\x00\x00@\xd2\xfb>\xd9A\x01\x00\x00\x00S\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\xad7\x00\x00(\xdd\x00\x00\xb1\xc3\x15\x00'
                    # b'                  \x00\x00{\xa5\x00\x00{\xa5\x00\x00)7\x00\x00\x00\x00@\xd2\xfb>\xd9A\x00\x00@\xd2\xfb>\xd9A\x01\x00\x00\x00S\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\xad7\x00\x00(\xdd\x00\x00\xb1\xc3\x15\x00\x0011000'
                    # lo que salio

                    # if superBloque_data == b'\x02\x00\x00\x00)7\x00\x00{\xa5\x00\x00{\xa5\x00\x00)7\x00\x00\x00\x00@\xd2\xfb>\xd9A\x00\x00@\xd2\xfb>\xd9A\x01\x00\x00\x00S\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\xad7\x00\x00(\xdd\x00\x00\xb1\xc3\x15\x00':
                        # print("chupala")

                    # Data es la info del superbloque
                    # print("###########################")
                    # b'\x01\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x98\x02\x00\x00'
                    # b'\x01\x00\x00\x00\x01\x00\x00\x00[\x00\x00\x00\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x01\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x98\x02\x00\x00'
                    # print("###########################")
                    # 
                    # print("ASDLÑFKAJSFDLKÑJ")
                    file.close()
            except Exception as e:
                print("\tERROR: No se pudo leer el disco en la ruta: " + self.path+", debido a: "+str(e))

        else:
            try: 
                mbr_format = "<iiiiB"
                mbr_size = struct.calcsize(mbr_format)

                # partition_format = "c2s3i3i16s"
                partition_format = "c2s3i3i16s"
                partition_size = struct.calcsize(partition_format)
                # print(particion_size)
                tamanioSuperBloque = struct.calcsize("<iiiiiddiiiiiiiiii")
                data = ""
                with open(self.path, "rb") as file:
                    mbr_data = file.read(mbr_size)
                    particion_data = file.read(partition_size)
                    superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                    # print(particion_data)
                    mbr = MBR()
                    (mbr.mbr_tamano, mbr.mbr_fecha_creacion, mbr.mbr_disk_signature, disk_fit, mbr.mbr_Partition_1, *_) = struct.unpack(mbr_format, mbr_data)
                    mbr.disk_fit = chr(disk_fit % 128) 

                    tamano_MBR = mbr.mbr_tamano
                    
                    partition1 = Particion()
                    particion_data = b'1PW'+ particion_data
                    particion_data = particion_data[:-2]
                    # print("PARTICON DATA")
                    # print(particion_data)
                    partition1.__setstate__(particion_data)
                    total = int(partition1.part_size)

                    """==================================="""
                    # print("============================")
                    # print(superBloque_data)
                    super_Bloque = SuperBloque()
                    
                    # print(len(superBloque_data))
                    # data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
                    # superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                    # superBloque_data = superBloque_data[:-6]
                    # print(superBloque_data)
                    data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
                    print(data)
                    # print("============================")
                    """==================================="""
                    # lo que deberia
                    # b'\x02\x00\x00\x00)7\x00\x00{\xa5\x00\x00{\xa5\x00\x00)7\x00\x00\x00\x00@\xd2\xfb>\xd9A\x00\x00@\xd2\xfb>\xd9A\x01\x00\x00\x00S\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\xad7\x00\x00(\xdd\x00\x00\xb1\xc3\x15\x00'
                    # b'                  \x00\x00{\xa5\x00\x00{\xa5\x00\x00)7\x00\x00\x00\x00@\xd2\xfb>\xd9A\x00\x00@\xd2\xfb>\xd9A\x01\x00\x00\x00S\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\xad7\x00\x00(\xdd\x00\x00\xb1\xc3\x15\x00\x0011000'
                    # lo que salio

                    # if superBloque_data == b'\x02\x00\x00\x00)7\x00\x00{\xa5\x00\x00{\xa5\x00\x00)7\x00\x00\x00\x00@\xd2\xfb>\xd9A\x00\x00@\xd2\xfb>\xd9A\x01\x00\x00\x00S\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x00\x00\x00\xad7\x00\x00(\xdd\x00\x00\xb1\xc3\x15\x00':
                        # print("chupala")

                    # Data es la info del superbloque
                    # print("###########################")
                    # b'\x01\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x98\x02\x00\x00'
                    # b'\x01\x00\x00\x00\x01\x00\x00\x00[\x00\x00\x00\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x00\x00\x80k\x06?\xd9A\x01\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x98\x02\x00\x00'
                    # print("###########################")
                    # 
                    file.close()
            except Exception as e:
                print("\tERROR: No se pudo leer el disco en la ruta: " + self.path+", debido a: "+str(e))

        return int(total), int(tamano_MBR)




    def repSuperBloque(self):
        try: 
            mbr_format = "<iiiiB"
            mbr_size = struct.calcsize(mbr_format)

            # partition_format = "c2s3i3i16s"
            partition_format = "c2s3i3i16s"
            partition_size = struct.calcsize(partition_format)
            # print(particion_size)
            tamanioSuperBloque = struct.calcsize("<iiiiiddiiiiiiiiii")
            data = ""
            with open(self.path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                # print(particion_data)
                mbr = MBR()
                (mbr.mbr_tamano, mbr.mbr_fecha_creacion, mbr.mbr_disk_signature, disk_fit, mbr.mbr_Partition_1, *_) = struct.unpack(mbr_format, mbr_data)
                mbr.disk_fit = chr(disk_fit % 128) 

                
                partition1 = Particion()
                particion_data = b'1PW'+ particion_data
                particion_data = particion_data[:-2]
                # print("PARTICON DATA")
                # print(particion_data)
                partition1.__setstate__(particion_data)
                

                """==================================="""
                # print("============================")
                # print(superBloque_data)
                super_Bloque = SuperBloque()
                
                # print(len(superBloque_data))
                # data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
                # print(data)
                # print("============================")
                """==================================="""

        except Exception as e:
            print("\tERROR: No se pudo leer el disco en la ruta: " + self.path+", debido a: "+str(e))

        
        print("\t============ SUPERBLOQUE ============")
        print("\tSB s_filesystem_type:", data[0])
        print("\tSB s_inodes_count:", (data[1]))
        print("\tSB s_block_count:", data[2])
        print("\tSB s_free_blocks_count:", data[3])
        print("\tSB s_free_inodes_count:", data[4])
        timestamp = data[5] #  Suponiendo que tienes una marca de tiempo en `timestamp`
        # print(timestamp/1000000000)
        fecha_formateada1 = 0
        if timestamp > 9999999:
            timestamp = 0
        try:
            fecha_y_hora = datetime.datetime.utcfromtimestamp(timestamp)
            # Formatear la fecha y hora según tus preferencias
            formato = "%Y-%m-%d %H:%M:%S"  # Puedes ajustar el formato como desees
            fecha_formateada1 = fecha_y_hora.strftime(formato)
        except Exception as e:
            print(e)
        
        print("\tSB s_mtime:", fecha_formateada1)


        timestamp = data[6] #  Suponiendo que tienes una marca de tiempo en `timestamp`
        try:
            fecha_y_hora = datetime.datetime.utcfromtimestamp(timestamp)
            # Formatear la fecha y hora según tus preferencias
            formato = "%Y-%m-%d %H:%M:%S"  # Puedes ajustar el formato como desees
            fecha_formateada2 = fecha_y_hora.strftime(formato)
        except Exception as e:
            print(e)
        
        print("\tSB s_umtime:", fecha_formateada2)
        print("\tSB s_mnt_count:", data[7])
        print("\tSB s_magic:", data[8])
        print("\tSB s_inode_size:", data[9])
        print("\tSB s_block_size:", data[10])
        print("\tSB s_first_ino:", data[11])
        print("\tSB s_first_blo:", data[12])
        print("\tSB s_bm_inode_start:", data[13])
        print("\tSB s_bm_block_start:", data[14])
        print("\tSB s_inode_start:", data[15])
        print("\tSB s_block_start:", data[16])
        print("=====================================")

        dot = f"""<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"> 
                <tr>
                    <td colspan="2">SUPERBLOQUE</td>
                </tr>
                <tr>
                    <td>s_filesystem_type</td>
                    <td>{data[0]}</td>
                </tr>
                <tr>
                    <td>s_inodes_count</td>
                    <td>{data[1]}</td>
                </tr>
                <tr>
                    <td>s_block_count</td>
                    <td>{data[2]}</td>
                </tr>
                <tr>
                    <td>s_free_blocks_count</td>
                    <td>{data[3]}</td>
                </tr>
                <tr>
                    <td>s_free_inodes</td>
                    <td>{data[4]}</td>
                </tr>
                <tr>
                    <td>s_mtime</td>
                    <td>{fecha_formateada1}</td>
                </tr>
                <tr>
                    <td>s_umtime</td>
                    <td>{fecha_formateada2}</td>
                </tr>
                <tr>
                    <td>s_mnt_count</td>
                    <td>{data[7]}</td>
                </tr>
                <tr>
                    <td>s_magic</td>
                    <td>{data[8]}</td>
                </tr>
                <tr>
                    <td>s_inode_size</td>
                    <td>{data[9]}</td>
                </tr>
                <tr>
                    <td>s_block_size</td>
                    <td>{data[10]}</td>
                </tr>
                <tr>
                    <td>s_first_ino</td>
                    <td>{data[11]}</td>
                </tr>
                <tr>
                    <td>s_first_blo</td>
                    <td>{data[12]}</td>
                </tr>
                <tr>
                    <td>s_bm_inode_start</td>
                    <td>{data[13]}</td>
                </tr>
                <tr>
                    <td>s_bm_block_start</td>
                    <td>{data[14]}</td>
                </tr>
                <tr>
                    <td>s_inode_start</td>
                    <td>{data[15]}</td>
                </tr>
                <tr>
                    <td>s_block_start</td>
                    <td>{data[16]}</td>
                </tr>
        </TABLE>>"""

        graficas.rep_SB(dot)


        
    def repInodes(self):
        dot = """<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"> """
        """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
        mbr_format = "<iiiiB"
        mbr_size = struct.calcsize(mbr_format)
        # partition_format = "c2s3i3i16s"
        partition_format = "c2s3i3i16s"
        partition_size = struct.calcsize(partition_format)
        data = ""
        pp = 0
        try: 
            with open(self.path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                # print(particion_data)
                mbr = MBR()
                (mbr.mbr_tamano, mbr.mbr_fecha_creacion, mbr.mbr_disk_signature, disk_fit, mbr.mbr_Partition_1, *_) = struct.unpack(mbr_format, mbr_data)
                mbr.disk_fit = chr(disk_fit % 128)
                partition1 = Particion()
                particion_data = b'1PW'+ particion_data
                particion_data = particion_data[:-2]
                # print("PARTICON DATA")
                # print(particion_data)
                partition1.__setstate__(particion_data)
                """==================================="""
                # print(superBloque_data)
                # super_Bloque = SuperBloque()
                # print(superBloque_data)
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
                # print(superBloque_data)
                # print("============================")
                """==================================="""

                
                file.close()
        except Exception as e:
            print("\tERROR: No se pudo leer el disco en la ruta: " +self.path+", debido a: "+str(e))

        # print(data)
        pp = int(data[15])
        inode = structs.Inodos()  # Crear una instancia de SuperBloque
        bytes_inodo= bytes(inode)  # Obtener los bytes de la instancia
        recuperado = bytearray(len(bytes_inodo))  # Crear un bytearray del mismo tamaño

        bandera = 0
        while bandera != -1:
            with open(self.path, "rb") as archivo:
                "prints del pp"
                print(pp)
                archivo.seek(pp)
                archivo.readinto(recuperado)

                inode.__setstate__(recuperado)
                print("INodes")
                print(f"UID: {inode.i_uid} , GID: {inode.i_gid} , Permisos: {inode.i_perm}")
                # print(f"Apuntadores 0-4:")
                # print({inode.i_block})

                timestamp = int(inode.i_atime) # Suponiendo que tienes una marca de tiempo en `timestamp`
                fecha_y_hora = datetime.datetime.utcfromtimestamp(timestamp)

                # Formatear la fecha y hora según tus preferencias
                formato = "%Y-%m-%d %H:%M:%S"  # Puedes ajustar el formato como desees
                fecha_formateada = fecha_y_hora.strftime(formato)

                dot += f"""
                <tr>
                    <td colspan="2">INODES</td>
                    
                </tr>
                <tr>
                    <td>i_uid</td>
                    <td>{inode.i_uid}</td>
                </tr>
                <tr>
                    <td>i_gid</td>
                    <td>{inode.i_gid}</td>
                </tr>
                <tr>
                    <td>i_size</td>
                    <td>{inode.i_size}</td>
                </tr>
                <tr>
                    <td>i_atime</td>
                    <td>{fecha_formateada}</td>
                </tr>
                <tr>
                    <td>i_ctime</td>
                    <td>{fecha_formateada}</td>
                </tr>
                <tr>
                    <td>i_mtime</td>
                    <td>{fecha_formateada}</td>
                </tr>
                <tr>
                    <td>i_block</td>
                    <td>{inode.i_block}</td>
                </tr>
                <tr>
                    <td>i_type</td>
                    <td>{inode.i_type}</td>
                </tr>
                <tr>
                    <td>i_perm</td>
                    <td>{inode.i_perm}</td>
                </tr>
                
            
                """
                # print(f"1: {inode.i_block[1]}")
                # print(f"2: {inode.i_block[2]}")
                # print(f"3: {inode.i_block[3]}")
                
                if inode.i_uid == -1 or inode.i_uid == 0:
                    bandera = -1
                else:
                    pp = pp + len(recuperado) 
            archivo.close()


        # print(dot)
        dot += """</TABLE>>"""
        graficas.rep_INODES(dot)
        """----------------------------"""




    
    def imprimirBloques(self, contador):
        dot = """"""
        mbr_format = "<iiiiB"
        mbr_size = struct.calcsize(mbr_format)
        # partition_format = "c2s3i3i16s"
        partition_format = "c2s3i3i16s"
        partition_size = struct.calcsize(partition_format)
        data = ""
        with open(self.path, "rb+") as file:
            mbr_data = file.read(mbr_size)
            particion_data = file.read(partition_size)
            
            """Block Start"""
            superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
            superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
            superBloque_data = superBloque_data[:-6]
            # print(superBloque_data)F
            data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
            # block_start = data[16]
            # print(block_start)
            bloques_carpetas = structs.BloquesCarpetas()
            bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
            recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño

            # recuperado += recuperado

            block_start = data[16]
            block_start += contador
            file.seek(block_start)
            file.readinto(recuperado)
            # print(recuperado)

            data_hex = bytearray(recuperado)
            # Convierte los datos hexadecimales en una lista de bytes
            byte_list = list(data_hex)

            # Imprime la lista de bytes
            # print(byte_list)

            # Define el formato esperado, que incluye una cadena (12s) y un entero (i)
            formato = "12s i"

            # Calcula el tamaño del struct en bytes para leer una vez a la vez
            tamanio_struct = struct.calcsize(formato)

            posicion = 0

            while posicion < len(data_hex):
                parte = data_hex[posicion:posicion + tamanio_struct]
                # print(tamanio_struct)
                # print(len(parte))
                if len(parte) < tamanio_struct:
                    break  # Si no quedan suficientes bytes para un registro completo, sal del bucle
                resultado = struct.unpack(formato, parte)
                cadena, entero = resultado
                # print(entero)
                # Crear un nuevo bytearray excluyendo los bytes \xFF
                filtered_byte_array = bytearray(byte for byte in cadena if byte != 0xFF)

                # print(filtered_byte_array)
                name = filtered_byte_array.decode('utf-8').rstrip("\0")

                
                print(f"Name: {name} | Inodo: {entero}")
                

                # if "." in name:
                #     name = "punto"

                name2 = name[:-4]

                dot += f"""
                    <tr>
                        <td colspan="2">BLOCK</td>
                    </tr>
                    <tr>
                        <td>NAME</td>
                        <td>{name2}</td>
                    </tr>
                    <tr>
                        <td>Inodo</td>
                        <td>{entero}</td>
                    </tr>
                    <tr>
                        <td colspan="2"> </td>
                    </tr>
                    """
                
                
                # if entero != -1:
                #     ultimo_b_inodo = entero
                posicion += tamanio_struct
                

             
               
            
            # Este código asume que los datos se organizan en registros alternados de 12 bytes para la cadena y 4 bytes para el entero, 
            # lo que corresponde al formato especificado en formato. Puedes ajustar el formato y el procesamiento según la estructura 
            # real de tus datos. Asegúrate de manejar los casos en los que no haya suficientes bytes para un registro 
            # completo o cuando la lectura llegue al final del bytearray.
            
            # imprimirBloques(path)
        # dot += """</TABLE>>"""
        # print(dot)
        # graficas.rep_BLOQUES(dot)
        return dot
    

    def rep_bm_inode(self, contador):
        dot = """"""
        mbr_format = "<iiiiB"
        mbr_size = struct.calcsize(mbr_format)
        # partition_format = "c2s3i3i16s"
        partition_format = "c2s3i3i16s"
        partition_size = struct.calcsize(partition_format)
        data = ""
        with open(self.path, "rb+") as file:
            mbr_data = file.read(mbr_size)
            particion_data = file.read(partition_size)
            
            """Block Start"""
            superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
            superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
            superBloque_data = superBloque_data[:-6]
            # print(superBloque_data)F
            data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
            # block_start = data[16]
            # print(block_start)
            bloques_carpetas = structs.BloquesCarpetas()
            bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
            recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño

            # recuperado += recuperado

            block_start = data[16]
            block_start += contador
            file.seek(block_start)
            file.readinto(recuperado)
            # print(recuperado)

            data_hex = bytearray(recuperado)
            # Convierte los datos hexadecimales en una lista de bytes
            byte_list = list(data_hex)

            # Imprime la lista de bytes
            # print(byte_list)

            # Define el formato esperado, que incluye una cadena (12s) y un entero (i)
            formato = "12s i"

            # Calcula el tamaño del struct en bytes para leer una vez a la vez
            tamanio_struct = struct.calcsize(formato)

            posicion = 0

            while posicion < len(data_hex):
                parte = data_hex[posicion:posicion + tamanio_struct]
                # print(tamanio_struct)
                # print(len(parte))
                if len(parte) < tamanio_struct:
                    break  # Si no quedan suficientes bytes para un registro completo, sal del bucle
                resultado = struct.unpack(formato, parte)
                cadena, entero = resultado
                # print(entero)
                # Crear un nuevo bytearray excluyendo los bytes \xFF
                filtered_byte_array = bytearray(byte for byte in cadena if byte != 0xFF)

                # print(filtered_byte_array)
                name = filtered_byte_array.decode('utf-8').rstrip("\0")

                
                # print(f"Name: {name} | Inodo: {entero}")
                

                if entero >= 0:
                    dot += """1"""
                else:
                    dot += """0"""
                
                
                # if entero != -1:
                #     ultimo_b_inodo = entero
                posicion += tamanio_struct
            
            # Este código asume que los datos se organizan en registros alternados de 12 bytes para la cadena y 4 bytes para el entero, 
            # lo que corresponde al formato especificado en formato. Puedes ajustar el formato y el procesamiento según la estructura 
            # real de tus datos. Asegúrate de manejar los casos en los que no haya suficientes bytes para un registro 
            # completo o cuando la lectura llegue al final del bytearray.
            
            # imprimirBloques(path)
        # dot += """</TABLE>>"""
        # print(dot)
        # graficas.rep_BLOQUES(dot)
        return dot