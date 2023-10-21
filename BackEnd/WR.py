from structs import MBR, Particion, EBR, SuperBloque
import struct
import structs
import pickle
import mount as Mount
import fdisk2
import os
import datetime
import time


cc = 0
pp = 0
block_start = 0



def mkfileInodo(path,archivo,usuario,permiso,tipo_AC,uid,gid,newPP,newBLOCKSTAR):
    global cc, pp, block_start

    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""
    try: 
        with open(path, "rb") as file:
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
            superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
            superBloque_data = superBloque_data[:-6]
            # print(superBloque_data)
            data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)
            # print(superBloque_data)
            # print("============================")
            """==================================="""
            file.close()


        startpp = -1
        notReadINODES = False
        if newPP == "":
            pp = data[15]
            startpp = pp
        else:
            pp = data[15]
            startpp = pp
            pp = int(newPP)
            notReadINODES = True



        startbs = -1
        notReadBlock = False
        bandera = False
        if newBLOCKSTAR == "":
            block_start = data[16]
            startbs = block_start
        else:
            block_start = data[16]
            startbs = block_start
            block_start = int(newBLOCKSTAR)
            notReadBlock = True
            bandera = True



        """
        ESTOS DE AQUI MOFICIAN EL START Y EL PP
        """
        if notReadINODES:
            imprimirINODES(startpp,path)
        else:
            """ IMPRIMIR INODES """
            imprimirINODES(pp,path)
            """"""

        if notReadBlock:
            """ CONTAR BLOQUES CARPETA Y RETORNAR SU CANTIDAD """
            cc = leerBloquesCarpetas(startbs,path)
        else:
            cc = leerBloquesCarpetas(block_start,path)
            """"""       
            """Lector Bloque ARCHIVOS """
            imprimirArchivos(block_start,path)
            """"""


        aa_pp, bb_bloc = ingresarInode(path, archivo, uid, gid, tipo_AC, permiso, bandera)
        return aa_pp, bb_bloc
        
    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))




def imprimirArchivos(block_start_a,path):
    global block_start
    block_start = block_start_a
    """Lector Bloque ARCHIVOS """
    bloque_archivo = structs.BloquesCarpetas()
    bytes_archivos= bytes(bloque_archivo)  # Obtener los bytes de la instancia
    recuperado = bytearray(len(bytes_archivos))  # Crear un bytearray del mismo tamaño
        
    try:            
        with open(path, "rb") as bfiles3:
            bfiles3.seek(block_start+len(recuperado))
            bfiles3.readinto(recuperado)
            bloque_archivo.b_content[0].b_name = recuperado[:64].decode('utf-8').rstrip('\0')
            print("safasdfa")
            print(bloque_archivo.b_content[0].b_name)
            print("safasdfa")
            bfiles3.close()
    except Exception as e:
        print(e)
    block_start += len(recuperado)
    """"""


def imprimirINODES(pp_a,path):
    """ INODES """
    global pp
    pp = pp_a
    inode = structs.Inodos()  # Crear una instancia de SuperBloque
    bytes_inodo= bytes(inode)  # Obtener los bytes de la instancia
    recuperado = bytearray(len(bytes_inodo))  # Crear un bytearray del mismo tamaño

    bandera = 0
    while bandera != -1:
        with open(path, "rb") as archivo:
            print(pp)
            archivo.seek(pp)
            archivo.readinto(recuperado)

            inode.__setstate__(recuperado)
            print(inode.i_perm)
            
            if inode.i_uid == -1:
                bandera = -1
            else:
                pp = pp + len(recuperado) 
        archivo.close()
        """"""    


def obtener_tamano_carpeta(carpeta):
    total_tamano = 0
    for dirpath, dirnames, filenames in os.walk(carpeta):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_tamano += os.path.getsize(filepath)
            
    return total_tamano


def leerBloquesCarpetas(block_start_a,path):
    global block_start
    block_start = block_start_a
    """ LEER LAS LISTA DE BLOQUES DE CARP  ETAS Y ARCHIVOS"""
    bloques_carpetas = structs.BloquesCarpetas()
    bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
    recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
    # recuperado = len(bytes(structs.BloquesCarpetas())) 
    contador_content = 0
    init_recu = 0
    # print(len(recuperado))
    bandera = 0
    try:
        while bandera != -1:
            with open(path, "rb") as bfiles:
                if init_recu >= len(recuperado):
                    bandera = -1
                bfiles.seek(block_start)
                bfiles.readinto(recuperado)

                bloques_carpetas.b_content[contador_content].b_name = recuperado[init_recu:init_recu+16].decode('utf-8').rstrip('\0')
                init_recu += 16
                bloques_carpetas.b_content[contador_content].b_inodo = struct.unpack("<i", recuperado[init_recu-4:init_recu])[0]

                
                print(bloques_carpetas.b_content[contador_content].b_name)
                print(bloques_carpetas.b_content[contador_content].b_inodo)
                contador_content += 1
                # bandera = -1
                bfiles.close()
    except Exception as e:
        str(e)
        print(f"Bloques Carpeta total: {contador_content}")
        # print(contador_content)
        return contador_content
    """"""


def ingresarInode(path, archivo, uid, gid, tipo_AC, permiso,bandera):
    global cc, pp, block_start
    # print("Block Start")
    # print(block_start)
    """INGRESO DE EL NUEVO INODE Y SUS BLOQUES"""
    ruta_carpetas = os.path.dirname(archivo)
    tamano_bytes = obtener_tamano_carpeta(ruta_carpetas)
    nombre_archivo = os.path.basename(archivo)

    # Creacion del bloque carpeta
    bloques_carpetas = structs.BloquesCarpetas()
    bytes_BLOQUES= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
    bloques_carpetas.b_content[cc].b_name = nombre_archivo
    bloques_carpetas.b_content[cc].b_inodo = cc

    # Creacion Bloque Archivo  
    bloque_archivo = structs.BloquesArchivos()
    recuperado = bytearray(len(bytes_BLOQUES))  # Crear un bytearray del mismo tamaño

    contenido = ""
    with open(archivo, "r") as archivo2:
            contenido = archivo2.read()
            # print(contenido)
            archivo2.close()
    bloque_archivo.b_content = contenido

    # CREACION DEL INODE
    inodeNuevo = structs.Inodos()
    inodeNuevo.i_uid   = uid
    inodeNuevo.i_gid   = gid
    inodeNuevo.i_size  = tamano_bytes
    inodeNuevo.i_atime = int(time.time())
    inodeNuevo.i_ctime = int(time.time())
    inodeNuevo.i_mtime = int(time.time())
    inodeNuevo.i_block[0] = int(bloques_carpetas.b_content[cc].b_inodo)
    inodeNuevo.i_block[1] = 1
    inodeNuevo.i_type  = tipo_AC
    inodeNuevo.i_perm  = permiso

    # print("PPPPPPPPPPPPPPPPPPPPP")
    # print(pp)
    # ESCRIBIR INODO
    with open(path, "rb+") as bfiles:
        bfiles.seek(pp)
        bfiles.write(bytes(inodeNuevo))
        bfiles.close()

    # print("PASAMOS")
    # ESCRIBIR BLOQUE CARPETA y ARCHIVO
    if bandera:
        block_start += 192
        with open(path, "rb+") as bfiles4:
            bfiles4.seek(block_start)
            bfiles4.write(bytes(bloques_carpetas))
            bfiles4.write(bytes(bloque_archivo))
            bfiles4.close()
    else:
        with open(path, "rb+") as bfiles4:
            bfiles4.seek(block_start+len(recuperado)*2)
            bfiles4.write(bytes(bloques_carpetas))
            bfiles4.write(bytes(bloque_archivo))
            bfiles4.close()

    # Creacion Bloque Archivo  
    inodeTemp = structs.Inodos()
    bytes_inode= bytes(inodeTemp)  # Obtener los bytes de la instancia
    recuperadoINODE = bytearray(len(bytes_inode))  # Crear un bytearray del mismo tamaño
    
    
    pp += len(recuperadoINODE)
    # print(f"pp : {pp}")

    block_start += len(recuperado)*2
    # print(f"Block: {block_start}")

    return str(pp), str(block_start)


"""
path = r'C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\DISCOS\disco.dsk'
archivo = r"C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\TXTS\users.txt"
aa, bb = mkfileInodo(path,archivo,"rol",444,1,5,4,"","")
print("==================")
print(f"aa: {aa}")
print(f"bb: {bb}")


dd, ff = mkfileInodo(path,archivo,"soy",251,1,5,4,aa,bb)
print("==================")
print(f"dd: {dd}")
print(f"ff: {ff}")
"""
