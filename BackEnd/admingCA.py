from structs import MBR, Particion, EBR, SuperBloque
import struct
import structs
import pickle
import mount as Mount
import os
import time

ultimo_b_inodo = -1
# BackEnd\backs\endinodo.txt


def salida_consola(texto):
        try:
            with open("BackEnd\contenidoTXT\salida_consola.txt","a") as archivo:
                    archivo.write(texto)
        except Exception as e: 
            print(str(e))

def escribirUltimoInodo(endInodo):
    with open("BackEnd/backs/endinodo.txt","w") as archivo:
        archivo.write(str(endInodo))

def leerUltimoInodo():
    contendio = ""
    with open("BackEnd/backs/endinodo.txt","r") as archivo:
        contendio = archivo.read()
    return int(contendio)




def leerBloquesFinal(path):
    global ultimo_b_inodo
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""

    info_user_txt = ""

    try:
        
            with open(path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)
                
                """Block Start"""
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
            # print(superBloque_data)F
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)

                block_start = data[16]
                # print(block_start)

                bloques_carpetas = structs.BloquesCarpetas()
                bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
                recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                

                # print(len(recuperado))
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

                # print("adsfañsldkfjasñkldfjadslkfj")
                # print(len(data_hex))
                while posicion < len(data_hex):
                    parte = data_hex[posicion:posicion + tamanio_struct]
                    # print(tamanio_struct)
                    # print(len(parte))
                    if len(parte) < int(tamanio_struct):
                        break  # Si no quedan suficientes bytes para un registro completo, sal del bucle
                    resultado = struct.unpack(formato, parte)
                    cadena, entero = resultado
                    """PRINT"""
                    # print(f"Name: {cadena.decode('utf-8')} | Inodo: {entero}")
                    if entero != -1:
                        ultimo_b_inodo = entero
                    posicion += tamanio_struct
                    
                # Este código asume que los datos se organizan en registros alternados de 12 bytes para la cadena y 4 bytes para el entero, 
                # lo que corresponde al formato especificado en formato. Puedes ajustar el formato y el procesamiento según la estructura 
                # real de tus datos. Asegúrate de manejar los casos en los que no haya suficientes bytes para un registro 
                # completo o cuando la lectura llegue al final del bytearray.
                file.close()

    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))

    
    bloque_final = block_start + 128
    # return (bloque_final)

    # Abre un archivo en modo escritura ('w' para escribir, 'a' para agregar al final)
    with open("BackEnd/backs/block_final.txt", 'w') as archivo:
        # Escribe una cadena en el archivo
        archivo.write(str(bloque_final))
        # print("Bloque Final Guardado")

    return bloque_final
    """"""


def obtenerPP():
    contenido = ""
    with open("BackEnd/backs/pp.txt","r") as pp_archivo:
        contenido = pp_archivo.read()
    return int(contenido)


def escribirUltimoPP(pp):
    with open("BackEnd/backs/pp.txt","w") as pp_archivo:
        pp_archivo.write(str(pp))

def mkfile(path, ruta_ingresar_archivo, fisrt, user, permisos, uid, gid, relleno_Archivo):
    global ultimo_b_inodo

    
    name_archivo = os.path.basename(ruta_ingresar_archivo)
    ruta = ruta_ingresar_archivo.replace(name_archivo, "")

    # print(name_archivo)
    # print(ruta)

    carpetas = ruta.split("/")
    del carpetas[0]
    del carpetas[-1]
    
    carpetas.append(name_archivo)

    bloque_start = 0
    s_inode_start = 0
    if fisrt:
        bloque_start = leerBloquesFinal(path)
        s_inode_start = firstObtenerPP(path)
    else:
        bloque_start = leerFinalSecond()
        s_inode_start = obtenerPP()
        ultimo_b_inodo = leerUltimoInodo()
        
        
    
    # print(type(bloque_start))
    # bloque_start = int(bloque_start)
    # print(type(bloque_start))


    print(carpetas)
    for nodo_c in carpetas:
        salida_consola(nodo_c+"\n")


    # print(bloque_start)


    # INFORMACION PA QUE NO CRASHEE
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""
    try:
            
            with open(path, "rb+") as file:
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
                
                """ AQUI SE EMPIEZA A ESCRIBIR LA INFO DE LA CARPETA """
                """                                                  """
                # Crear instancia de BloquesCarpetas
                block_carpeta = structs.BloquesCarpetas()

                # Obtener el inicio del bloque
                # bloque_start = leerBloquesFinal(path)

                # Obtener el último PP
                # s_inode_start = escribirUltimoPP(path)

                for indice, valor in enumerate(carpetas):
                    print(str(ultimo_b_inodo) + " - " + valor)
                    if indice == 4:
                        break

                    block_carpeta.b_content[indice].b_name = valor
                    block_carpeta.b_content[indice].b_inodo = ultimo_b_inodo

                    if indice == len(carpetas) - 1:
                        # print(str(ultimo_b_inodo + 1) + " - " + name_archivo)
                        block_carpeta.b_content[indice].b_name = name_archivo
                        block_carpeta.b_content[indice].b_inodo = ultimo_b_inodo + 1

                        # Crear inodo de la carpeta
                        inode = structs.Inodos()
                        inode.i_uid = int(uid)
                        inode.i_gid = int(gid)
                        inode.i_size = 0
                        inode.i_atime = int(time.time())
                        inode.i_ctime = int(time.time())
                        inode.i_mtime = int(time.time())
                        inode.i_type = 0
                        inode.i_perm = int(permisos)

                        for cont, _ in enumerate(inode.i_block):
                            if _ == -1:
                                inode.i_block[cont] = ultimo_b_inodo + 1
                                break

                        # Escribir el inodo en el disco
                        with open(path, "rb+") as bfiles:
                            bfiles.seek(s_inode_start)
                            bfiles.write(bytes(inode))

                        s_inode_start += 101

                        # # Crear inodo del archivo
                        # inode.i_type = 1
                        # inode.i_size = 0
                        # inode.i_block[0] = 0

                        # # Escribir el inodo en el disco
                        # with open(path, "rb+") as bfiles:
                        #     bfiles.seek(s_inode_start)
                        #     bfiles.write(bytes(inode))

                        # s_inode_start += 101
                        escribirUltimoPP(s_inode_start)
                        escribirUltimoInodo((ultimo_b_inodo+1))
                        # print("PUTA")

                    else:
                        block_carpeta.b_content[indice].b_name = valor
                        block_carpeta.b_content[indice].b_inodo = ultimo_b_inodo

                        inode = structs.Inodos()
                        inode.i_uid = int(uid)
                        inode.i_gid = int(gid)
                        inode.i_size = 0
                        inode.i_atime = int(time.time())
                        inode.i_ctime = int(time.time())
                        inode.i_mtime = int(time.time())
                        inode.i_type = 0
                        inode.i_perm = int(permisos)

                        for cont, _ in enumerate(inode.i_block):
                            if _ == -1:
                                inode.i_block[cont] = ultimo_b_inodo + 1

                        ultimo_b_inodo += 1

                        with open(path, "rb+") as bfiles:
                            bfiles.seek(s_inode_start)
                            bfiles.write(bytes(inode))

                        s_inode_start += 101

                # with open(path, "rb+") as file:
                file.seek(bloque_start)
                # file.write(bytes(block_carpeta))
                # bloque_start += 64

            # Crear instancia de BloquesArchivos
                block_archivos = structs.BloquesArchivos()
                block_archivos.b_content = relleno_Archivo


                file.write(bytes(block_carpeta))
                file.write(block_archivos.__bytes__())
                bloque_start += 128

    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))
                            
    with open("BackEnd/backs/block_final.txt", 'w') as archivo:
                    archivo.write(str(bloque_start))
    """"""
    

def b_block(carpetas):
    contenido_actual = ""
    with open('BackEnd/Reportes/b_block.txt', 'r') as archivo:
        contenido_actual = archivo.read()

    bas = ""
    for c in carpetas:
        bas += "1"
    
    contenidoCompleto = bas + contenido_actual
    with open('BackEnd/Reportes/b_inode.txt', 'w') as archivo:
        archivo.write(contenidoCompleto)
    
    with open('BackEnd/Reportes/b_block.txt', 'w') as archivo:
        archivo.write(contenidoCompleto)


def leerFinalSecond():
    contenido = ""
    with open("BackEnd/backs/block_final.txt", 'r') as archivo:
        # Escribe una cadena en el archivo
        contenido = archivo.read()
        # print("Bloque Final Guardado")
    return int(contenido)






def firstObtenerPP(path):
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""
    pp = 0
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
    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))

    pp = int(data[15])
    inode = structs.Inodos()  # Crear una instancia de SuperBloque
    bytes_inodo= bytes(inode)  # Obtener los bytes de la instancia
    recuperado = bytearray(len(bytes_inodo))  # Crear un bytearray del mismo tamaño

    bandera = 0
    while bandera != -1:
        with open(path, "rb") as archivo:
            "prints del pp"
            # print(pp)
            archivo.seek(pp)
            archivo.readinto(recuperado)

            inode.__setstate__(recuperado)
            # print(inode.i_perm)
            
            if inode.i_uid == -1:
                bandera = -1
            else:
                pp = pp + len(recuperado) 
        archivo.close()

    # with open("MAINS/backs/pp.txt","w") as pp_archivo:
    #     pp_archivo.write(str(pp))

    return pp
    """"""  


def imprimirInodes(path):
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""
    pp = 0
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
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))

    # print(data)
    pp = int(data[15])
    inode = structs.Inodos()  # Crear una instancia de SuperBloque
    bytes_inodo= bytes(inode)  # Obtener los bytes de la instancia
    recuperado = bytearray(len(bytes_inodo))  # Crear un bytearray del mismo tamaño

    bandera = 0
    while bandera != -1:
        with open(path, "rb") as archivo:
            "prints del pp"
            print(pp)
            archivo.seek(pp)
            archivo.readinto(recuperado)

            inode.__setstate__(recuperado)
            print(f"UID: {inode.i_uid} , GID: {inode.i_gid} , Permisos: {inode.i_perm}")
            print(f"Apuntadores 0-4:")
            print({inode.i_block})
            # print(f"1: {inode.i_block[1]}")
            # print(f"2: {inode.i_block[2]}")
            # print(f"3: {inode.i_block[3]}")
            
            if inode.i_uid == -1 or inode.i_uid == 0:
                bandera = -1
            else:
                pp = pp + len(recuperado) 
        archivo.close()
    """----------------------------"""


def imprimirBloques(path, contador):
    
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""
    with open(path, "rb+") as file:
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

        # print(len(data_hex))
        while posicion < len(data_hex):
            parte = data_hex[posicion:posicion + tamanio_struct]
            # print(tamanio_struct)
            # print(len(parte))
            if len(parte) < int(tamanio_struct):
                break  # Si no quedan suficientes bytes para un registro completo, sal del bucle
            resultado = struct.unpack(formato, parte)
            cadena, entero = resultado
            # print(entero)
            # Crear un nuevo bytearray excluyendo los bytes \xFF
            filtered_byte_array = bytearray(byte for byte in cadena if byte != 0xFF)

            # print(filtered_byte_array)
            name = filtered_byte_array.decode('utf-8')

            
            print(f"Name: {name} | Inodo: {entero}")
            
            
            # if entero != -1:
            #     ultimo_b_inodo = entero
            posicion += tamanio_struct

            

        # Este código asume que los datos se organizan en registros alternados de 12 bytes para la cadena y 4 bytes para el entero, 
        # lo que corresponde al formato especificado en formato. Puedes ajustar el formato y el procesamiento según la estructura 
        # real de tus datos. Asegúrate de manejar los casos en los que no haya suficientes bytes para un registro 
        # completo o cuando la lectura llegue al final del bytearray.
        
        # imprimirBloques(  path)
        

# def cat(path, listaArchivos):


def buscarCAT(path, buscar,contador):

    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""
    with open(path, "rb+") as file:
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

        # print(len(data_hex))
        while posicion < len(data_hex):
            parte = data_hex[posicion:posicion + tamanio_struct]
            # print(tamanio_struct)
            # print(len(parte))
            if len(parte) < int(tamanio_struct):
                break  # Si no quedan suficientes bytes para un registro completo, sal del bucle
            resultado = struct.unpack(formato, parte)
            cadena, entero = resultado
            # print(entero)
            # Crear un nuevo bytearray excluyendo los bytes \xFF
            filtered_byte_array = bytearray(byte for byte in cadena if byte != 0xFF)
            # print(cadena)
            # print(filtered_byte_array)
            name = ""
            try:
                # Supongamos que filtered_byte_array contiene la secuencia de bytes
                name = filtered_byte_array.decode('utf-8').rstrip("\0")
                # print(f"Nombre limpio: {name}")
            except UnicodeDecodeError as e:
                pass
                # Manejar una excepción si la decodificación UTF-8 falla
                # print(f"Error al decodificar UTF-8: {e}")
            except Exception as ex:
                pass
                # Manejar cualquier otra excepción que pueda ocurrir
                # print(f"Error inesperado: {ex}")


            # print(f"Name: {name} | Inodo: {entero}")
            if name == buscar:
                # print("encontrado")
                # print(name)
                file.seek(block_start+64)
                recuperado2 = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                file.readinto(recuperado2)
                # resultado2 = struct.unpack(formato, parte)
                soy = recuperado2.decode("utf-8".rstrip("\0"))
               
                # print(recuperado2)
                print(soy)


            # if entero != -1:
            #     ultimo_b_inodo = entero
            posicion += tamanio_struct
            
        # Este código asume que los datos se organizan en registros alternados de 12 bytes para la cadena y 4 bytes para el entero, 
        # lo que corresponde al formato especificado en formato. Puedes ajustar el formato y el procesamiento según la estructura 
        # real de tus datos. Asegúrate de manejar los casos en los que no haya suficientes bytes para un registro 
        # completo o cuando la lectura llegue al final del bytearray.
        
        # imprimirBloques(path)


def reporteFILE(path, buscar,contador,path_rep):
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""
    ya = ""
    with open(path, "rb+") as file:
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

        # print(len(data_hex))
        while posicion < len(data_hex):
            parte = data_hex[posicion:posicion + tamanio_struct]
            # print(tamanio_struct)
            # print(len(parte))
            if len(parte) < int(tamanio_struct):
                break  # Si no quedan suficientes bytes para un registro completo, sal del bucle
            resultado = struct.unpack(formato, parte)
            cadena, entero = resultado
            # print(entero)
            # Crear un nuevo bytearray excluyendo los bytes \xFF
            filtered_byte_array = bytearray(byte for byte in cadena if byte != 0xFF)
            # print(cadena)
            # print(filtered_byte_array)
            name = ""
            try:
                # Supongamos que filtered_byte_array contiene la secuencia de bytes
                name = filtered_byte_array.decode('utf-8').rstrip("\0")
                # print(f"Nombre limpio: {name}")
            except UnicodeDecodeError as e:
                pass
                # Manejar una excepción si la decodificación UTF-8 falla
                # print(f"Error al decodificar UTF-8: {e}")
            except Exception as ex:
                pass
                # Manejar cualquier otra excepción que pueda ocurrir
                # print(f"Error inesperado: {ex}")


            # print(f"Name: {name} | Inodo: {entero}")
            if name == buscar:
                # print("encontrado")
                # print(name)
                file.seek(block_start+64)
                recuperado2 = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                file.readinto(recuperado2)
                # resultado2 = struct.unpack(formato, parte)
                soy = recuperado2.decode("utf-8").rstrip("\0")
               
                # print(recuperado2)
                # print(soy)
                # Abre el archivo en modo escritura ('w')
                try:
                    with open(path_rep, 'w') as archivo:
                        # Escribe los datos en el archivo
                        archivo.write(soy)

                    print("Archivo creado y datos escritos con éxito.")
                except Exception as e:
                    print(f"Error al crear y escribir en el archivo: {e}")


                


            # if entero != -1:
            #     ultimo_b_inodo = entero
            posicion += tamanio_struct
    
         


"""================================== PRUEBAS ================================== """
# path = r"/home/rol/Tareas/PR1/MIA_PR1/Discos/disco.dsk"
# bloqueFinal = leerBloquesFinal(path)
# print(bloqueFinal)


# mkfile(path,r"/home/user/sol/archivo.txt",True,"rol","555","2","2","0123456789")
# mkfile(path,r"/home/mis documentos/archivo2.txt",False,"rol","222","2","2","0123")
# mkfile(path,r"/home/mis_2/a.txt",False,"rol","417","2","2","0123456789")
# mkfile(path,r"/home/user/soy.txt",False,"rol","417","2","2","hola")

# imprimirInodes(path)

""""""
# contendio = ""
# with open("MAINS/backs/endinodo.txt","r") as archivo:
#     contendio = archivo.read()
   
# cont = 0
# for _ in range(int(contendio)):
#     imprimirBloques(path, cont)
#     cont += 64+64


# lista = ["archivo.txt"]
# contador = 0
# for arch_list in lista:
#     # print(arch_list)
#     for _ in range(int(contendio)):
#         buscarCAT(path, arch_list,contador)
#         contador += 128
#     contador = 0


# lista = ["archivo.txt"]
# contador = 0
# data = ""
# for arch_list in lista:
#     # print(arch_list)
#     for _ in range(int(contendio)):
#         reporteFILE(path, arch_list,contador,r"/home/rol/Tareas/PR1/MIA_PR1/repo.txt")
#         contador += 128
#     contador = 0


