from structs import MBR, Particion, EBR, SuperBloque
import struct
import structs
import pickle
import mount as Mount
import fdisk2
import os
import datetime
import time
import sys


class SalirDeBucles(Exception):
    pass

def salida_consola(texto):
        try:
            with open("/home/ubuntu/MIA_PR2/BackEnd/contenidoTXT/salida_consola.txt","a") as archivo:
                    archivo.write(texto)
        except Exception as e: 
            print(str(e)) 

def login(path, user, password):
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""

    info_user_txt = ""

    try:
        f = False
        for _ in range(1):
            with open(path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)

                """Block Start"""
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)

                block_start = data[16]
                # print(block_start)

                bloques_carpetas = structs.BloquesArchivos()
                bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
                recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                
                file.seek(block_start+64)
                file.readinto(recuperado)
                # print(recuperado)
                
                """ARCHIVOS"""
                data = struct.unpack("<64s", recuperado)
                contenido_desempaquetado = data[0].decode('utf-8').rstrip('\0')
                # print(data)
                info_user_txt = contenido_desempaquetado
                file.close()

    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))


    # Haz algo con el contenido del archivo
    info_user_txt = info_user_txt.rstrip("\n")
    # print(info_user_txt)
    matriz1 = info_user_txt.split("\n")
    # print(matriz1)
    
    cola = []
    for x in matriz1:
        linea = x.split(",")
        cola.append(linea)
        
    # print(cola)
    i = 0
    x = 0
    encontrado = False
    uid = -1
    gid = -1
    for i in range(len(cola)):
        for x in range(len(cola[i])):
            if len(cola[i]) > 4:
                # print(cola[i][x])
                try:
                    if cola[i][x] == user and cola[i][x+1] == password:
                        # print(user)
                        # print(cola[i][x+1])
                        encontrado = True
                        uid = int(cola[i][0])
                        # print(cola[i][2])
                        gid = buscarGrupoYDevolver(cola[i][2], info_user_txt)
                        break
                except Exception as e: 
                    print(str(e))
    return encontrado, uid, gid

    """FIN"""
    
def buscarGrupoYDevolver(grupo, contenido):
    # Haz algo con el contenido del archivo
    # print(contenido)
    matriz1 = contenido.split("\n")
    # print(matriz1)

    cola = []
    for x in matriz1:
        linea = x.split(",")
        cola.append(linea)
        
    

    # print(cola)
    i = 0
    x = 0
    e_ar = False
    # print(len(cola))
    try:
        for i in range(len(cola)):
            for x in range(len(cola[i])):
                # print(cola[i])
                if len(cola[i]) < 4:
                    # print("sdfa "+cola[i][2])
                    if cola[i][2] == grupo:
                        # print(f"El Grupo Ingresado: - {grupo} - ya Existe")
                        e_ar = False
                        return cola[i][0]
                        raise SalirDeBucles
                    else:
                        e_ar = True
                        indice = cola[i][x-2]
    except SalirDeBucles:
        pass  # Maneja la excepción para salir de todos los bucles



"""MKGR"""

def mkgrp(path, name):
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""

    info_user_txt = ""

    try:
        f = False
        for _ in range(1):
            with open(path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)

                """Block Start"""
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)

                block_start = data[16]
                # print(block_start)

                bloques_carpetas = structs.BloquesArchivos()
                bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
                recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                
                block_start += 64
                file.seek(block_start)
                file.readinto(recuperado)
                # print(recuperado)
                
                """ARCHIVOS"""
                data = struct.unpack("<64s", recuperado)
                contenido_desempaquetado = data[0].decode('utf-8').rstrip('\0')
                # print(data)
                info_user_txt = contenido_desempaquetado
                file.close()

    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))

    indice = 0
    info_user_txt = info_user_txt.rstrip("\n")
    # print(info_user_txt)
    matriz1 = info_user_txt.split("\n")
    # print(matriz1)

    
    

    cola = []
    for x in matriz1:
        linea = x.split(",")
        cola.append(linea)
        
    # print(cola)
    i = 0
    x = 0
    e_ar = False
    # print(len(cola))
    try:
        for i in range(len(cola)):
            for x in range(len(cola[i])):
                # print(cola[i])
                if len(cola[i]) < 4:
                    # print("sdfa "+cola[i][2])
                    if cola[i][2] == name:
                        print(f"El Grupo Ingresado: - {name} - ya Existe")
                        salida_consola(f"El Grupo Ingresado: - {name} - ya Existe\n")
                        e_ar = False
                        raise SalirDeBucles
                    else:
                        e_ar = True
                        indice = cola[i][x-2]
    except SalirDeBucles:
        pass  # Maneja la excepción para salir de todos los bucles
    # print(indice)
    cua = int(indice)
    cua += 1
    data = ("\n"+str(cua)+",G,"+name)
    # print(e_ar)
    data = info_user_txt + data
    if e_ar:
        escribirDATA(path, data)
        print(f"Grupo {name} registrado correctamente")
        salida_consola(f"Grupo {name} registrado correctamente\n")


    """"""



def rmgrp(path, name):
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""

    info_user_txt = ""

    try:
        f = False
        for _ in range(1):
            with open(path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)

                """Block Start"""
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)

                block_start = data[16]
                # print(block_start)

                bloques_carpetas = structs.BloquesArchivos()
                bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
                recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                
                file.seek(block_start+64)
                file.readinto(recuperado)
                # print(recuperado)
                
                """ARCHIVOS"""
                data = struct.unpack("<64s", recuperado)
                contenido_desempaquetado = data[0].decode('utf-8').rstrip('\0')
                # print(data)
                info_user_txt = contenido_desempaquetado
                file.close()

    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))


    contenido = info_user_txt

    info_user_txt = info_user_txt.rstrip("\n")
    # print(info_user_txt)
    matriz1 = info_user_txt.split("\n")
    # print(matriz1)

    cola = []
    for x in matriz1:
        linea = x.split(",")
        cola.append(linea)
        

    
    # print(cola)
    i = 0
    x = 0
    e_ar = False
    cont_temp = ""
    # print(len(cola))
    try:
        for i in range(len(cola)):
            for x in range(len(cola[i])):
                # print(cola[i])
                if len(cola[i]) < 4:
                    # print("sdfa "+cola[i][2])
                    if cola[i][2] == name:
                        # print(f"El Grupo Ingresado: - {name} - Encontrado")
                        e_ar = True
                        # break
                        cola[i][0] = "0"
                cont_temp += cola[i][x] + "," 
            cont_temp = cont_temp[:-1] + "\n"
    except SalirDeBucles:
        pass  # Maneja la excepción para salir de todos los bucles

    # print(cont_temp[:-1])

    if e_ar:
        escribirDATA(path, cont_temp[:-1])
        print(f"Grupo {name} Eliminado correctamente")
        salida_consola(f"Grupo {name} Eliminado correctamente\n")
    else:
        print("Grupon Ingresado no Existente")
        salida_consola("Grupo Ingresado no Existente\n")
    """ FIN """


def mkusr(path, user, password, grp):
    indice = 0
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""

    info_user_txt = ""

    try:
        f = False
        for _ in range(1):
            with open(path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)

                """Block Start"""
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)

                block_start = data[16]
                # print(block_start)

                bloques_carpetas = structs.BloquesArchivos()
                bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
                recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                
                file.seek(block_start+64)
                file.readinto(recuperado)
                # print(recuperado)
                
                """ARCHIVOS"""
                data = struct.unpack("<64s", recuperado)
                contenido_desempaquetado = data[0].decode('utf-8').rstrip('\0')
                # print(data)
                info_user_txt = contenido_desempaquetado
                file.close()

    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))

    contenido = info_user_txt

    info_user_txt = info_user_txt.rstrip("\n")
    # print(info_user_txt)
    matriz1 = info_user_txt.split("\n")
    # print(matriz1)


    cola = []
    for x in matriz1:
        linea = x.split(",")
        cola.append(linea)
        
    # print(cola)
    i = 0
    x = 0
    e_ar = False
    grp_bool = False
    # print(len(cola))
    try:
        for i in range(len(cola)):
            for x in range(len(cola[i])):
                if len(cola[i]) < 4:
                    if cola[i][2] == grp and cola[i][0] != "0":
                        grp_bool = True
                        indice = cola[i][0]

                elif len(cola[i]) > 3:
                    # print("sdfa "+cola[i][2])
                    if cola[i][3] == user:
                        print(f"El Usuario Ingresado: - {user} - ya Existe")
                        salida_consola(f"El Usuario Ingresado: - {user} - ya Existe\n")
                        e_ar = False
                        raise SalirDeBucles
                    else:
                        e_ar = True
                        
                # indice = cola[i][0]
    except SalirDeBucles:
        pass  # Maneja la excepción para salir de todos los bucles

    # print(indice)
    cua = int(indice)
    # cua += 1
    data = ("\n"+str(cua)+",U,"+grp+","+user+","+password)
    # print(data)
    data = info_user_txt + data
    # print(data)
    if e_ar and grp_bool:
        # print(data)
        escribirDATA(path, data)
        print(f"Usuario {user} registrado correctamente")
        salida_consola(f"Usuario {user} registrado correctamente\n")
    """FIN"""



def rmusr(path, user):
    indice = 0
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""

    info_user_txt = ""

    try:
        f = False
        for _ in range(1):
            with open(path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)

                """Block Start"""
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)

                block_start = data[16]
                # print(block_start)

                bloques_carpetas = structs.BloquesArchivos()
                bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
                recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                
                file.seek(block_start+64)
                file.readinto(recuperado)
                # print(recuperado)
                
                """ARCHIVOS"""
                data = struct.unpack("<64s", recuperado)
                contenido_desempaquetado = data[0].decode('utf-8').rstrip('\0')
                # print(data)
                info_user_txt = contenido_desempaquetado
                file.close()

    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))

    contenido = info_user_txt

    info_user_txt = info_user_txt.rstrip("\n")
    # print(info_user_txt)
    matriz1 = info_user_txt.split("\n")
    # print(matriz1)

    cola = []
    for x in matriz1:
        linea = x.split(",")
        cola.append(linea)

    
    # print(cola)
    i = 0
    x = 0
    e_ar = False
    cont_temp = ""
    # print(len(cola))
    try:
        for i in range(len(cola)):
            for x in range(len(cola[i])):
                # print(cola[i])
                if len(cola[i]) > 4:
                    # print("sdfa "+cola[i][2])
                    if cola[i][3] == user:
                        # print(f"El Grupo Ingresado: - {name} - Encontrado")
                        e_ar = True
                        # break
                        cola[i][0] = "0"
                cont_temp += cola[i][x] + "," 
            cont_temp = cont_temp[:-1] + "\n"
    except SalirDeBucles:
        pass  # Maneja la excepción para salir de todos los bucles

    # print(cont_temp[:-1])

    if e_ar:
        escribirDATA(path,cont_temp[:-1])
        print(f"Usuario {user} Eliminado correctamente")
        salida_consola(f"Usuario {user} Eliminado correctamente\n")
    else:
        print("Usuario Ingresado no Existente")
        salida_consola("Usuario Ingresado no Existente\n")



""" ##################### LECTOR Y ESCRITOR ##########################"""
def escribirDATA(path, data_sobreescribir):
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""

    info_user_txt = ""

    try:
        f = False
        for _ in range(1):
            with open(path, "rb+") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)

                """Block Start"""
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)

                block_start = data[16]
                # print(block_start)

                bloques_carpetas = structs.BloquesArchivos()
                bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
                recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                
                bloques_carpetas.b_content = data_sobreescribir

                file.seek(block_start+64)
                file.write(bytes(bloques_carpetas))
                # print(recuperado)
                file.close()
                

    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))





def leerDATA(path):
    """ LECTOR DEL SUPERBLOQUE PARA ENCONTRAR LOS STARST """
    mbr_format = "<iiiiB"
    mbr_size = struct.calcsize(mbr_format)
    # partition_format = "c2s3i3i16s"
    partition_format = "c2s3i3i16s"
    partition_size = struct.calcsize(partition_format)
    data = ""

    info_user_txt = ""

    try:
        f = False
        for _ in range(1):
            with open(path, "rb") as file:
                mbr_data = file.read(mbr_size)
                particion_data = file.read(partition_size)

                """Block Start"""
                superBloque_data = file.read(struct.calcsize("<iiiiiddiiiiiiiiii"))
                superBloque_data = b'\x02\x00\x00\x00)7' + superBloque_data 
                superBloque_data = superBloque_data[:-6]
                # print(superBloque_data)
                data = struct.unpack("<iiiiiddiiiiiiiiii", superBloque_data)

                block_start = data[16]
                # print(block_start)

                bloques_carpetas = structs.BloquesArchivos()
                bytes_carpetas= bytes(bloques_carpetas)  # Obtener los bytes de la instancia
                recuperado = bytearray(len(bytes_carpetas))  # Crear un bytearray del mismo tamaño
                
                file.seek(block_start+64)
                file.readinto(recuperado)
                # print(recuperado)
                # print(len(recuperado))
                
                """ARCHIVOS"""
                data = struct.unpack("<64s", recuperado)
                contenido_desempaquetado = data[0].decode('utf-8').rstrip('\0')
                print(contenido_desempaquetado)
                salida_consola("\n=========Administracion Usuarios y Grupos=========\n"+contenido_desempaquetado+"\n==================\n")
                info_user_txt = contenido_desempaquetado
                file.close()

    except Exception as e:
        print("\tERROR: No se pudo leer el disco en la ruta: " +path+", debido a: "+str(e))



"""================================== PRUEBAS ================================== """
# path = r"C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\DISCOS\disco.dsk"

# LOGIN
# encontrado, uid, gid = login(path,"root","123")
# print(encontrado)
# print(uid)
# print(gid)

# CREAR GRUPO
# mkgrp(path,"pal")

# # ELIMINAR GRUPO
# rmgrp(path, "pal")

# # CREAR USUARIO
# mkusr(path,"oscar","777","pal")

# # ELIMINAR USUARIO
# rmusr(path,"oscar")

# leerDATA(path)

