#!/usr/bin/env python3

import ply.lex as lex
import ply.yacc as yacc
from mkdisk import MkDisk
from rep import reporte
from fdisk2 import FDisk
from mount import *
import adminUG
import adminCarpetas
from mkfs import MKFS
import structs
import admin
import admingCA
import re
import time
import graficas

# Definición de tokens
tokens = (
    'MKDISK',
    'FDISK',
    'SIZE',
    'UNIT',
    'PATH',
    'TYPE',
    'NAME',
    'NUM',
    'LETRA_MKDISK',
    'IGUAL',
    'GUION',
    'DIR',
    'LETRA_FDISK',
    'REP',
    'RMDISK',
    'FIT',
    'LETRAS_FIT',
    'DELETE',
    'ADD',
    'UNMOUNT',
    'MOUNT',
    'ID',
    'MKFS',
    'FS',
    'FS_VAL',
    'LOGIN',
    'USER',
    'PASS',
    'LOGOUT',
    'MKGRP',
    'RMGRP',
    'GRP',
    'MKUSR',
    'RMUSR',
    'CONT',
    'MKFILE',
    'R',
    'FILE1',
    'FILE2',
    'REMOVE',
    'CAT',
    'EDIT',
    'RENAME',
    'COPY',
    'DESTINO',
    'MKDIR',
    'EXECUTE',
    'RUTA',
    'STRING',
    'PAUSE',
    'CADENA',
)

reserved = {
    'mkdisk' : 'MKDISK',
    'fdisk' : 'FDISK',
    'size' : 'SIZE',
    'unit' : 'UNIT',
    'path' : 'PATH',
    'type' : 'TYPE',
    'name' : 'NAME',
    'num' : 'NUM',
    'letra_mkdisk' : 'LETRA_MKDISK',
    'igual' : 'IGUAL',
    'guion' : 'GUION',
    'dir' : 'DIR',
    'letra_fdisk' : 'LETRA_FDISK',
    'rep' : 'REP',
    'rmdisk' : 'RMDISK',
    'fit' : 'FIT',
    'letras_fit' : 'LETRAS_FIT',
    'delete' : 'DELETE',
    'add' : 'ADD',
    'unmount' : 'UNMOUNT',
    'mount' : 'MOUNT',
    'id' : 'ID',
    'mkfs' : 'MKFS',
    'fs' : 'FS',
    'fs_val' : 'FS_VAL',
    'login' : 'LOGIN',
    'user' : 'USER',
    'pass' : 'PASS',
    'logout' : 'LOGOUT',
    'mkgrp' : 'MKGRP',
    'rmgrp': 'RMGRP',
    'mkusr' : 'MKUSR',
    'rmusr' : 'RMUSR',
    'r' : 'R',
    'mkfile' : 'MKFILE',
    'file1' : 'FILE1',
    'file2' : 'FILE2',
    'cont' : 'CONT',
    'cat' : 'CAT',
    'remove': 'REMOVE',
    'edit' : 'EDIT',
    'remove' : 'REMOVE',
    'copy' : 'COPY',
    'destino' : 'DESTINO',
    'mkdir' : 'MKDIR',
    'execute' : 'EXECUTE',
    'string' : 'STRING',
    'ruta' : 'RUTA',
    'grp' : 'GRP'
    # Agrega todas tus palabras clave aquí
}


# Expresiones regulares para tokens simples
t_MKDISK = r'mkdisk'
t_FDISK = r'fdisk'
t_R = r'r'
t_MKFILE = r'mkfile'
t_REP = r'rep'
t_SIZE = r'size'
t_UNIT = r'unit'
t_PATH = r'path'
t_TYPE = r'type'
t_GRP = r'grp'
t_CONT = r'cont'
t_NAME = r'name'
t_PAUSE = r'pause'
t_DELETE = r'delete'
t_MKFS = r'mkfs'
t_MKGRP = r'mkgrp'
t_MKUSR = r'mkusr'
t_RMUSR  = r'rmusr'
t_FS = r'fs'
t_FS_VAL = r'2fs|3fs'
t_MOUNT = r'mount'
t_UNMOUNT = r'unmount'
t_LOGIN = r'login'
t_LOGOUT = r'logout'
t_USER = r'user'
t_PASS = r'pass'
t_ID = r'id'
t_ADD = r'add'
t_GUION = r'-'
t_LETRA_MKDISK = r'[MK]'
t_LETRA_FDISK = r'[BKMEPL]'
t_FIT = r'fit'
t_LETRAS_FIT = r'wf|bf|ff'
t_IGUAL = r'='
t_RMDISK = r'rmdisk'
t_RMGRP = r'rmgrp'
t_CAT = r'cat'
t_REMOVE = r'remove'
t_EDIT = r'edit'
t_RENAME = r'rename'
t_COPY = r'copy'
t_DESTINO = r'destino'
t_MKDIR = r'mkdir'
t_EXECUTE = r'execute'
t_RUTA = r'ruta'


def t_FILE1(t):
    r'file[0-9]'
    return t

def t_FILE2(t):
    r'file[0-9][0-9]*'

# Expresión regular para directorio
def t_DIR(t):
    r'=\/[a-zA-Z0-9_\/\.]+ | =\"\/[a-zA-Z0-9_\/\.]+\"'

    # r'=C:\\[^\\]+(\\[^\\]+)*\\[^.]+\.[a-z]+ | =\"C:\\[^\\]+(\\[^\\]+)*\\[^.]+\.[a-z]+\"'

    # r'=C:\\[^\\]+(\\[^\\]+)*\\[^.]+\.[a-zA-Z0-9]+ | \"=C:\\[^\\]+(\\[^\\]+)*\\[^.]+\.[a-zA-Z0-9]+\"'
    if t.value.endswith('"') or t.value.endswith("'"):
        t.value = t.value[2:-1]  # Eliminar las comillas alrededor de la cadena
        # print(t)
    else:
        t.value = t.value[1:]
    # r'[^\\]+(\\[^\\]+)*\\[^.]+\.[a-zA-Z0-9]+'
    # r'\\[a-zA-Z0-9_\\\.]+'
    return t

def t_STRING(t):
    r'=(\"[^\"]*\") | =([a-zA-Z0-9_]+[a-zA-Z0-9]*)'
    if t.value.endswith('"') or t.value.endswith("'"):
        t.value = t.value[2:-1]  # Eliminar las comillas alrededor de la cadena
    else:
        t.value = t.value[1:]
    return t


# Expresiones regulares de cadena para que no entre en conflico con los tokens simples
# def t_CADENA(t):
#     r'(\"[^"]*\"|\'[^\']*\')'
#     if t.value.startswith('"') or t.value.startswith("'"):
#         t.value = t.value[1:-1]  # Eliminar las comillas alrededor de la cadena
#     # Verifica si la cadena es una palabra clave
#     # t.type = reserved.get(t.value, 'CADENA')
#     return t

# def t_NUMERO(t):
#     r'\d+'  # Reconoce secuencias de dígitos como números
#     t.type = 'NUM'
#     t.value = int(t.value)  # Convierte la cadena a un entero
#     return t

def t_COMENTARIOS(t):
    r'\#.*'
    pass  # Ignorar comentarios


# Ignorar caracteres en blanco y saltos de línea
t_ignore = ' \t\n'

# Manejo de errores
def t_error(t):
    print("Carácter ilegal:", t.value[0])
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Variables para almacenar los valores de los comandos
command = ""
size = ""
unit = ""
path = ""
type = ""
name = ""
unit_fkdisk = ""
fit = ""
add = 0
id = ""
numParticion = 1
fs_val = "ext2"

sesion_Iniciada = False
user = ""
password = ""
permiso_Usuario = "777"
uid = -1
gid = -1

mount = Mount()
path_mount = ""
name_mount = ""

path_del_disco = r"BackEnd\Discos\path_del_disco.txt"
with open(r"BackEnd\Discos\path_del_disco.txt","r") as xde:
    path_del_disco = xde.read()



bandera_mkfile = False
pp = -1
block_start = -1

first = True
e_local = False


# Reglas de gramática
def p_comando_mkdisk(p):
    '''comando : MKDISK atributosm'''
    global command, size, unit, path, fit, path_del_disco
    command = "mkdisk"
    print(f"Comando: {command}")
    for atributo in p[2]:
        # print(f"{atributo[0]}: {atributo[1]}")
        if atributo[0] == "size":
            size = atributo[1]
        elif atributo[0] == "unit":
            unit = atributo[1]
        elif atributo[0] == "path":
            path = atributo[1]
        elif atributo[0] == "fit":
            fit = atributo[1]

    # Eliminando las comillas del path
    if path.startswith("\""):
        path = path[1:-1]

    if fit == "":
        fit = "ff"

    # path = path[1:]
    # size = size[1:]
    # unit = unit[1:]
    # fit  = fit[1:]
    # imprimir valores ingresados
    print("Size: "+str(size))
    print("Unit: "+str(unit))
    print("Fit: "+str(fit))
    print("Path: "+str(path))
    texto = f"""Comando. MKDISK
Size: {str(size)}
Unit: {str(unit)}
Fit: {str(fit)}
Path: {str(path)}
"""
    salida_consola(texto)
    
    path_del_disco = path
    nombre_archivo = os.path.basename(path)
    ruta_PR2 = r"BackEnd\Discos" + "\\" + nombre_archivo
    # creacion del disco con los valores ingresados
    disk = MkDisk()
    disk.path = ruta_PR2
    disk.size = size
    disk.unit = unit
    disk.fit  = fit
    disk.create()


    with open(r"BackEnd\Discos\path_del_disco.txt","w") as xde:
        xde.write(path)
    # reseteo de las variables para su uso futuro
    size = ""
    unit = ""
    path_del_disco = ruta_PR2
    # mkdisk -size=5 -fit=wf -unit=M -path=C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\DISCOS\disco.dsk
    # mkdisk -size=5 -fit=wf -unit=M -path=/home/rol/Tareas/PR1/MIA_PR1/Discos/disco2.dsk

def p_atributosM(p):
    '''atributosm : atributosm atributom
                 | atributom'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoM(p):
    '''atributom : GUION PATH DIR
                 | GUION FIT STRING
                 | GUION UNIT STRING
                 | GUION SIZE STRING'''
    p[0] = (p[2], p[3])



# Reglas para el comando fdisk
def p_comando_fdisk(p):
    '''comando : FDISK atributos'''
    global command, size, unit_fkdisk, path, name, type, fit, add, path_del_disco, e_local
    command = "fdisk"
    delete = ""
    print(f"Comando: {command}")
    for atributo in p[2]:
        # print(f"{atributo[0]}: {atributo[1]}")
        if atributo[0] == "size":
            size = atributo[1]
        elif atributo[0] == "unit":
            unit_fkdisk = atributo[1]
        elif atributo[0] == "type":
            type = atributo[1]
        elif atributo[0] == "path":
            path = atributo[1]
        elif atributo[0] == "name":
            name = atributo[1]
        elif atributo[0] == "fit":
            fit = atributo[1]
        elif atributo[0] == "add":
            add = atributo[1]
        elif atributo[0] == "delete":
            delete = "FULL"
    
    # Eliminando las comillas del path
    if path.startswith("\""):
        path = path[1:-1]


    if add != 0 and delete.lower() == 'full':
        add = 0
        delete = ""
        print("el comando ADD y DELETE no se pueden ejecutar al mismo tiempo")
    else: 

        if fit == "":
            fit = "ff"

        # Imprimiendo las variables
        print("Size: "+str(size))
        print("Unit: "+str(unit_fkdisk))
        print("Path: "+str(path))
        print("Name: "+str(name))
        print("Type: "+str(type))
        print("Fit: "+fit)
        print(f"Add: {add}")
        print("Delete: "+delete)
        text_sali = f"""
Comando: FDISK
Size: {str(size)}
Unit: {unit_fkdisk}
Path: {path}
Name: {name}
Type: {type}
Fit: {fit}
Add: {add}
Delete: {delete}\n"""
        salida_consola(text_sali)

        nombre_archivo = os.path.basename(path)
        ruta_PR2 = r"BackEnd\Discos" + "\\" + nombre_archivo


        if type.lower() == "e":
            repo = reporte()
            repo.path = path_del_disco
            try:
                repo.repSuperBloque()
            except Exception as e: 
                print(str(e))
            e_local = True


        partition = FDisk()
        partition.delete = delete
        partition.size = int(size)
        partition.type = type
        partition.unit = unit_fkdisk
        partition.path = ruta_PR2
        partition.name = name
        partition.fit = fit
        partition.add = add
        partition.fdisk()

    size = ""
    unit_fkdisk = ""
    path = ""
    name = ""
    type = ""
    # fdisk -type=E -path=C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\DISCOS\disco.dsk -unit=M -name="Particion1" -size=1
    # fdisk -type=P -path=/home/rol/Tareas/PR1/MIA_PR1/Discos/Disco2.dsk -unit=M -name=hola -size=2


def p_atributos(p):
    '''atributos : atributos atributo
                 | atributo'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributo(p):
    '''atributo : GUION PATH DIR
                | GUION TYPE STRING
                | GUION UNIT STRING
                | GUION NAME STRING
                | GUION SIZE STRING
                | GUION FIT STRING
                | GUION ADD STRING
                | GUION DELETE'''
    if len(p) == 3:
        p[0] = (p[2], p[1])
    else:
        p[0] = (p[2], p[3])





def p_comando_rmdisk(p):
    '''comando : RMDISK GUION PATH DIR'''
    global path

    path = p[4]
    # Eliminando las comillas del path
    if path.startswith("\""):
        path = path[1:-1]

    print(f"Ruta del archivo a eliminar: {path}\n")
    salida_consola(f"Ruta del archivo a eliminar: {path}")
    nombre_archivo = os.path.basename(path)
    ruta_PR2 = r"BackEnd\Discos" + "\\" + nombre_archivo
    rm = RmDisk()
    rm.path = ruta_PR2
    rm.remove()


def p_comando_mount(p):
    '''comando : MOUNT atributos_mount'''
    global numParticion, path_mount, name_mount, mount, path_del_disco
    # MONTA UNA PARTICION DEL DISCO, como: saber?
    # inicioParticion = "44"
    command = "mount"
    print(f"Comando: {command}")
    for atributo in p[2]:
        if atributo[0] == "path":
            path_mount = atributo[1] 
        elif atributo[0] == "name":
            name_mount = atributo[1]
    
    texto_rp = """"""
    if name_mount == "" or path_mount == "":
        print("Se necesita el path y el name para ejecutar el comando Mount")
        texto_rp = """Se necesita el path y el name para ejecutar el comando Mount"""
    else:
        print("Path: "+str(path_mount))
        print("Name de la particion a usar: "+str(name_mount))
        texto_rp=f"""
Comando: Mount
Path: {path_mount}
Name: {name_mount} \n"""
        salida_consola(texto_rp)

        nombre_archivo = os.path.basename(path_mount)
        ruta_PR2 = r"BackEnd\Discos" + "\\" + nombre_archivo

        mount.mount(ruta_PR2, name_mount)
        mount.listaMount()

        # mount -path=/home/rol/Tareas/PR1/MIA_PR1/Discos/disco2.dsk -name=hola
    path_del_disco = ruta_PR2
    with open(r"BackEnd\Discos\path_del_disco.txt","w") as xde:
        xde.write(path_del_disco)

def p_atributos_mount(p):
    '''atributos_mount : atributos_mount atributo_mm
                 | atributo_mm'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributo_mount(p):
    '''atributo_mm : GUION PATH DIR
                   | GUION NAME STRING'''
    p[0] = (p[2], p[3])



def p_comando_unmount(p):
    '''comando : UNMOUNT GUION ID STRING'''
    global path_mount, name_mount, mount
    # id = ""
    command = "unmount"
    texto_rp=f"""
Comando: UnMount
ID: {p[4]} \n"""
    print(f"Comando: {command}")
    id = p[4]
    print(f"ID: {id}")
    salida_consola(texto_rp)
    mount.unmount(id)
    mount.listaMount()
    


def p_comando_mkfs(p):
    '''comando : MKFS atributos_mkfs'''
    global fs_val, id, type, mount
    
    type_mkfs = "Full"
    fs_val = "2fs"
    command = "mkfs"
    for atributo in p[2]:
        if atributo[0] == "id":
            id = atributo[1]
        elif atributo[0] == "type":
            type = atributo[1]
        elif atributo[0] == "fs":
            fs_val = atributo[1]

    if id != "":
        print(f"Comando: {command}")
        print(f"ID: {id}")
        print(f"Type: {type_mkfs}")
        print(f"Fs: {fs_val}")

        text_rp = f"""
Comando: MKFS
ID: {id}
Type: {type_mkfs}
Fs: 2FS\n"""

        type_mkfs = "Full"
        fs_val = "2fs"
        salida_consola(text_rp)

        fileSystem = MKFS(mount)
        tks = [id,type,fs_val]
        fileSystem.mkfs(tks)

        # mkfs -id=441disco2 -type=FUll -fs=2fs

    else: 
        print("El comando MKFS requiere obligatoriamente de un id")
        salida_consola("El comando MKFS requiere obligatoriamente de un id")
        # mkfs -id="parte 1" -type=P -fs=2fs


def p_atributos_mkfs(p):
    '''atributos_mkfs : atributos_mkfs atributosSolo_mkfs
                        | atributosSolo_mkfs'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_mkfs(p):
    '''atributosSolo_mkfs : GUION ID STRING
                            | GUION TYPE STRING'''
    p[0] = (p[2], p[3])



def p_comando_login(p):
    '''comando : LOGIN atributos_login'''
    global sesion_Iniciada, user, password, id, permiso_Usuario, uid, gid, path_del_disco
    command = "login"
    print(f"Command: {command}")
    for atributo in p[2]:
        if atributo[0] == "id":
            id = atributo[1]
        elif atributo[0] == "user":
            user = atributo[1]
        elif atributo[0] == "pass":
            password = atributo[1]

    if user != "" and id != "" and password != "":
        print(f"User: {user}")
        print(f"Pass: {password}")
        print(f"ID: {id}")
        
        
        encontrado, uid, gid = admin.login(path_del_disco,user,password)
        # print(encontrado)
        sesion_Iniciada = encontrado

        if encontrado:
            if user == "root" or user == "ROOT":
                permiso_Usuario = "777"
            else:
                permiso_Usuario = "664"
            print("    Usuario Encontrado")
            print(f"    Bienvendio {user}.")
        else:
            print("Usuario NO encontrado")
            user = ""
    else:
        print("Porfavor ingrese todos los datos del user, password, id\n")
    # login -user=root -pass=123 -id=441disco
    # login -user="mi usuario" -pass="mi pwd" -id=061Disco1


def p_atributos_login(p):
    '''atributos_login : atributos_login atributosSolo_login
                        | atributosSolo_login'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_login(p):
    '''atributosSolo_login :  GUION USER STRING
                            | GUION PASS STRING
                            | GUION ID STRING'''
    p[0] = (p[2], p[3])


# SALE DE LA SESION
def p_comando_logout(p):
    '''comando : LOGOUT'''
    global user, id, password, sesion_Iniciada
    print(f"SALIENDO de la Sesion usuario {user} ...")
    user = ""
    id = ""
    password = ""
    sesion_Iniciada = False



# ESCRIBE un grupo en el users.txt 
# solo lo puede usar el ROOT
def p_comando_mkgrp(p):
    '''comando : MKGRP GUION NAME STRING'''
    global sesion_Iniciada, user, path_del_disco
    name = p[4]
    if user == "root" or user == "ROOT":
        if sesion_Iniciada:
            print("Comando: MKGRP usuario ROOT")
            salida_consola("Comando: MKGRP usuario ROOT\n")
            admin.mkgrp(path_del_disco, name)
            admin.leerDATA(path_del_disco)
        else:
            print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
    else:
        print("Solo el usuario ROOT con su sesion iniciada puede ejecutar este comando")
        print("Porfavor INICIE SESION como ROOT para ejecutar este comando")


def p_comando_rmgrp(p):
    '''comando : RMGRP GUION NAME STRING'''
    global sesion_Iniciada, user, path_del_disco
    name = p[4]
    if user == "root" or user == "ROOT":
        if sesion_Iniciada:
            print("Comando: RMGRP usuario ROOT")
            salida_consola("Comando: RMGRP usuario ROOT")
            admin.rmgrp(path_del_disco,name)
            admin.leerDATA(path_del_disco)
        else:
            print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
    else:
        print("Solo el usuario ROOT con su sesion iniciada puede ejecutar este comando")
        print("Porfavor INICIE SESION como ROOT para ejecutar este comando")


def p_comando_mkusr(p):
    '''comando : MKUSR atributos_mkusr'''       
    global sesion_Iniciada, sesion_Iniciada, path_del_disco
    name_ingresar = ""
    pass_ingresar = ""
    grp = ""
    for atributo in p[2]:
        if atributo[0] == "user":
            name_ingresar = atributo[1]
        elif atributo[0] == "grp":
            grp = atributo[1]
        elif atributo[0] == "pass":
            pass_ingresar = atributo[1]

 
    if user == "root" or user == "ROOT":
        if sesion_Iniciada:
            print("Comando: MKUSR usuario ROOT")
            # adminUG.mkusr(name_ingresar,pass_ingresar,grp)
            salida_consola("Comando: MKUSR usuario ROOT\n")
            admin.mkusr(path_del_disco,name_ingresar,pass_ingresar,grp)
            admin.leerDATA(path_del_disco)
        else:
            print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
    else:
        print("Solo el usuario ROOT con su sesion iniciada puede ejecutar este comando")
        print("Porfavor INICIE SESION como ROOT para ejecutar este comando")



def p_atributos_mkusr(p):
    '''atributos_mkusr : atributos_mkusr atributosSolo_mkusr
                        | atributosSolo_mkusr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_mkusr(p):
    '''atributosSolo_mkusr :  GUION USER STRING
                            | GUION PASS STRING
                            | GUION GRP STRING'''
    p[0] = (p[2], p[3])




def p_comando_rmusr(p):
    '''comando : RMUSR GUION NAME STRING'''
    global sesion_Iniciada, user, sesion_Iniciada, path_del_disco
    name_ingresar = p[4]
    

    if user == "root" or user == "ROOT":
        if sesion_Iniciada:
            print("Comando: RMUSR usuario ROOT")
            salida_consola("Comando: RMUSR usuario ROOT\n")
            admin.rmusr(path_del_disco,name_ingresar)
            admin.leerDATA(path_del_disco)
        else:
            print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
    else:
        print("Solo el usuario ROOT con su sesion iniciada puede ejecutar este comando")
        print("Porfavor INICIE SESION como ROOT para ejecutar este comando")






# MKFILE
def p_comando_mkfile(p):
    '''comando : MKFILE atributos_mkfile'''
    global permiso_Usuario, user, sesion_Iniciada, bandera_mkfile, pp, block_start, path_del_disco, first, uid, gid
    
    path_mkfile =""
    size_mkfile = ""
    cont_mkfile = ""
    r = False
    for atributo in p[2]:
        if atributo[0] == "path":
            path_mkfile = atributo[1]
        elif atributo[0] == "size":
            size_mkfile = atributo[1]
        elif atributo[0] == "cont":
            cont_mkfile = atributo[1]
        elif atributo[0] == "r":
            r = True
    

    if user != "":
        if sesion_Iniciada:
            print(F"Comando: MKFILE usuario {user}")
            print(f"Path: {path_mkfile}")
            print(f"Size: {size_mkfile}")
            print(f"Cont: {cont_mkfile}")
            print(f'R : {r}')

            texto_r2 = f"""
Comando MKFILE: usuario {user}
Path: {path_mkfile}
Size: {size_mkfile}
Cont: {cont_mkfile}
R: {r}\n"""
            
            salida_consola(texto_r2)
            # nombre_archivo = os.path.basename(path_mount)
            # ruta_PR2 = r"BackEnd\Discos" + "\\" + nombre_archivo


            if size_mkfile == "":
                size_mkfile = "0"

            if path_mkfile == "":
                print("Porfavor Ingrese el Path Obligatorio del comando MKFILE")
                salida_consola("Porfavor Ingrese el Path Obligatorio del comando MKFILE\n")
            elif int(size_mkfile) < 0:
                print("No se aceptan numeros negativos en size")
                salida_consola("No se aceptan numeros negativos en size\n")
            else:
                print("Ejecutando...")
                salida_consola("Ejecutando...\n")
                # print("Comando MKFILE")
                caracteres_escritos = 0
                cont = 0
                secuencia = "0123456789"
                relleno_archivo = ""
                while caracteres_escritos < int(size_mkfile):
                        if cont > 9:
                            cont = 0
                        relleno_archivo += (secuencia[cont])
                        caracteres_escritos += 1
                        cont += 1
                
                # aa, bb = adminCarpetas.crearArchivo(path_del_disco,path_mkfile,int(size_mkfile),r,cont_mkfile,user,permiso_Usuario,uid,gid,bandera_mkfile,pp,block_start)
                # pp = aa
                # block_start = bb
                # bandera_mkfile = True
             
                admingCA.mkfile(path_del_disco,path_mkfile,first,user,permiso_Usuario,uid,gid,relleno_archivo)
                # admingCA.imprimirInodes(path_del_disco)
                first = False
                
                # mkfile -size=15-path==/home/user/docs/a.txt -r
    

        else:
            print("Porfavor INICIE SESION para ejecutar este comando")
    else:
        print("Porfavor INICIE SESION para ejecutar este comando")



def p_atributos_mkfile(p):
    '''atributos_mkfile : atributos_mkfile atributosSolo_mkfile
                        | atributosSolo_mkfile'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_mkfile(p):
    '''atributosSolo_mkfile : GUION PATH DIR
                            | GUION SIZE STRING
                            | GUION CONT STRING
                            | GUION R'''
    if len(p) == 3:
        p[0] = (p[2], p[1])
    else:
        p[0] = (p[2], p[3])

# =======================================================================================================

# PROBAR EN LINUX
# PROBAR EN LINUX
# PROBAR EN LINUX
# PROBAR EN LINUX
# PROBAR EN LINUX
# PROBAR EN LINUX
# PROBAR EN LINUX

def p_comando_cat(p):
    '''comando : CAT listaFilesCAT'''   
    global permiso_Usuario, user, sesion_Iniciada, path_del_disco
    
    path_cat =""
    size_cat= ""
    cont_cat = ""
    arreglar = ""
    first_file = ""
    pattern = r"[a-zA-Z0-9_\s]+\.[a-zA-Z0-9]+"

    for atributo in p[2]:
        if atributo[0][:-1] == "file":
            # print(atributo[0] + " " + atributo[1])
            first_file = atributo[0]
            arreglar = atributo[1]

    # print(first_file)
    # print(arreglar)

    lista_cat = []
    matches = re.findall(pattern, arreglar)
    if matches:
        # Si se encuentran coincidencias, imprimir cada una de ellas
        # for match in matches:
        #     print("Coincidencia encontrada:", match)
        #     lista_cat.append(match)
        lista_cat = matches
    # else:
    #     print("No se encontraron coincidencias en el texto.")

    contendio = ""
    with open("MAINS/backs/endinodo.txt","r") as archivo:
        contendio = archivo.read()

    # lista = ["puta.txt","a.txt","archivo3.txt","soy.txt"]
    contador = 0
    # path_del_disco = r"C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\DISCOS\disco.dsk"
    for arch_list in lista_cat:
        # print(arch_list)
        for _ in range(int(contendio)):
            admingCA.buscarCAT(path_del_disco,arch_list,contador)
            contador += 128
        contador = 0
    
    # print(arreglar)
    # arreglar = arreglar.split(" ")
    # l_arreglado = []
    # pepe = (first_file, arreglar[0].replace("\"",""))
    # l_arreglado.append(pepe)

    # name_File = ""
    # dir_path = ""
    # for data in arreglar:
    #     name_File = data[0:7]
    #     name_File = name_File.replace("-","")
    #     name_File = name_File.replace("=","")
    #     dir_path = data[7:]
    #     dir_path = dir_path.replace("=","")
    #     dir_path = dir_path.replace("\"","")       
    #     pepe = (name_File, dir_path)
    #     l_arreglado.append(pepe)
            
    # # print(name_File)
    # # print(dir_path)
    # del l_arreglado[1]
    # # for i in l_arreglado:
    # #     print(i)
    # print(l_arreglado)
    # adminCarpetas.cat(l_arreglado)

# cat -file1="C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\G\sxaa.txt" -file2="C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\G\hola to.txt" -file3="C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\G\sxaa.txt"


def p_listaFilesCAT(p):
    '''listaFilesCAT : listaFilesCAT atributosSolo_CAT
                        | atributosSolo_CAT'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

# =============probar 
def p_atributoSolo_CAT(p):
    '''atributosSolo_CAT : GUION FILE2 STRING
                         | GUION FILE1 STRING'''
    p[0] = (p[2], p[3])

#  =======================================================================================================



# REMOVE
def p_comando_remove(p):
    '''comando : REMOVE GUION PATH DIR'''
    global user, password, id, permiso_Usuario, sesion_Iniciada

    if sesion_Iniciada:
        adminCarpetas.remover(p[5])
    else:
        print("Porfavor INICIE SESION como ROOT para ejecutar este comando")



# EDIT
def p_comando_edit(p):
    """comando : EDIT listas_edit"""

    path_edit = ""
    cont_edit = ""
    for atributo in p[2]:
        if atributo[0] == "path":
            path_edit = atributo[1]
        elif atributo[0] == "cont":
            cont_edit = atributo[1]
    
    if user != "":
        if path_edit != "" and cont_edit != "":
            if sesion_Iniciada:
                print(f"Comando EDIT")
                print(f"Path {path_edit}")
                print(f"Cont: {cont_edit}")
                adminCarpetas.edit(path_edit,cont_edit)
            else:
                print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
        else:
            print("EL COMANDO EDIT NECISTA DE UN PATH Y UN CONT")
    else:
        print("Porfavor INICIE SESION para ejecutar este comando")


def p_listaFilesEDIT(p):
    '''listas_edit : listas_edit atributosSolo_EDIT
                        | atributosSolo_EDIT'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_EDIT(p):
    '''atributosSolo_EDIT : GUION PATH DIR
                         |  GUION CONT DIR'''
    p[0] = (p[2], p[3])



# RENAME
def p_comando_rename(p):
    """comando : RENAME lista_rename"""

    path_rename = ""
    name_rename = ""
    for atributo in p[2]:
        if atributo[0] == "path":
            path_rename = atributo[1]
        elif atributo[0] == "name":
            name_rename = atributo[1]

    if user != "":
        if path_rename != "" and name_rename != "":
            if sesion_Iniciada:
                print(f"Comando EDIT")
                print(f"Path {path_rename}")
                print(f"Name: {name_rename}")
                adminCarpetas.rename(path_rename,name_rename)
            else:
                print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
        else:
            print("EL Comando RENAME necesita de un Path y Name")
    else:
        print("Porfavor INICIE SESION para ejecutar este comando")
    
    
    
def p_listaFilesRENAME(p):
    '''lista_rename : lista_rename atributosSolo_RENAME
                        | atributosSolo_RENAME'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_RENAME(p):
    '''atributosSolo_RENAME : GUION PATH DIR
                            | GUION NAME STRING'''
    p[0] = (p[2], p[3])



# MKDIR
def p_comando_mkdir(p):
    """comando : MKDIR lista_mkdir"""
    global user, sesion_Iniciada

    path_mkdir = ""
    r_mkdir = False
    
    for atributo in p[2]:
        if atributo[0] == "path":
            path_mkdir = atributo[1]
        elif atributo[0] == "r":
            r_mkdir = True

    if user != "":
        if path_mkdir != "":
            if sesion_Iniciada:
                print(f"Comando EDIT")
                print(f"Path {path_mkdir}")
                print(f"R: {r_mkdir}")
                adminCarpetas.mkdir(path_mkdir,r_mkdir)
            else:
                print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
        else:
            print("EL Comando MKDIR necesita de un Path")
    else:
        print("Porfavor INICIE SESION para ejecutar este comando")


def p_listaFilesMKDIR(p):
    '''lista_mkdir : lista_mkdir atributosSolo_MKDIR
                        | atributosSolo_MKDIR'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_MKDIR(p):
    '''atributosSolo_MKDIR : GUION PATH DIR
                           | GUION R'''
    if len(p) == 3:
        p[0] = (p[2], p[1])
    else:
        p[0] = (p[2], p[3])



# COPY
def p_comando_copy(p):
    """comando : COPY lista_copy"""
    global user, sesion_Iniciada, password

    path_copy = ""
    destino_copy = ""
    
    for atributo in p[2]:
        if atributo[0] == "path":
            path_copy = atributo[1]
        elif atributo[0] == "destino":
            destino_copy = atributo[1]

    if user != "":
        if path_copy != "" and destino_copy != "":
            if sesion_Iniciada:
                print(f"Comando EDIT")
                print(f"Path {path_copy}")
                print(f"Destino: {destino_copy}")
                adminCarpetas.copy(path_copy,destino_copy)
            else:
                print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
        else:
            print("EL Comando MKDIR necesita de un Path")
    else:
        print("Porfavor INICIE SESION para ejecutar este comando")


def p_listaFilesCOPY(p):
    '''lista_copy : lista_copy atributosSolo_COPY
                        | atributosSolo_COPY'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_COPY(p):
    '''atributosSolo_COPY : GUION PATH DIR
                          | GUION DESTINO DIR'''

    p[0] = (p[2], p[3])



def p_comando_execute(p):
    """comando : EXECUTE GUION PATH DIR"""
    path_ejecutar = p[4]
    print(path_ejecutar)
    contenido = ""
    
    with open(path_ejecutar,"r") as archivo:
            contenido = archivo.read()
    
   
    # Número de segundos de retraso
    # COMENTARIO AJFDÑAKDJFAÑFK
    delay_seconds = 2  # Cambia esto al valor deseado
    print(f"=-=-=-=-= Ejecutando comandos en {path_ejecutar} =-=-=-=-=")
    
    comandos = contenido.split("\n")
    for comando in comandos:
        print(comando)
        parser.parse(comando)
        time.sleep(delay_seconds)
    

# reglas comadno REP
def p_comando_rep(p):
    '''comando : REP lista_rep'''
    global path_del_disco, e_local
    
    id_rep = ""
    path_rep = ""
    name_rep = ""
    ruta_rep = ""


    for atributo in p[2]:
        if atributo[0] == "path":
            path_rep = atributo[1]
        elif atributo[0] == "name":
            name_rep = atributo[1]
        elif atributo[0] == "id":
            id_rep = atributo[1]
        elif atributo[0] == "ruta":
            ruta_rep = atributo[1]

    
        if path_rep != "":
                print(f"Comando REP")
                print(f"Path {path_rep}")
                print(f"ID: {id_rep}")
                print(f"NAME: {name_rep}")

                if path_rep[1:3] != "tmp":
                    path_del_disco = r"/tmp/"+str(id_rep[3:])+".dsk" 

                lts_p_reportes = ["mbr","disk","inode","journaling","block","bm_inode","bm_block","tree","sb","file","ls"]
                repo = reporte()
                repo.path = path_del_disco
                
                if (name_rep).lower() == "mbr":
                    print("")
                    print("Creando Reporte MBR")
                    repo.repMBR()
                elif name_rep.lower() == "disk":
                    print("")
                    print("CReando Reporte DISK")

                    total_size = -1
                    size_part1 = -1
                    size_part2= -1
                    size_part2 = -1
                    size_part4 = -1
                    final_part = 0
                    for _ in range(4):
                        size, total_size = repo.repFDISK2(final_part)
                        final_part += 44

                        if _ == 0:
                            size_part1 = size
                        elif _ == 1:
                            size_part2 = size
                        elif _ == 2:
                            size_part3 = size
                        elif _ == 3:
                            size_part4 = size

                    print(f"MBR tamaño: {total_size}")
                    print(f"PART1 : {size_part1}")
                    print(f"PART2 : {size_part2}")
                    print(f"PART3 : {size_part3}")
                    print(f"PART4 : {size_part4}")
                    graficas.rep_FDISK(total_size,size_part1,size_part2,size_part3,size_part4)
                    print("")
                elif name_rep.lower() == "inode":
                    repo.repInodes()
                    print("")
                elif name_rep.lower() == "journaling":

                    graficas.rep_Journaling()
                    print("")
                elif name_rep.lower() == "block":
                    contendio = ""
                    with open("BackEnd/backs/endinodo.txt","r") as archivo:
                        contendio = archivo.read()
                    
                    cont = 0
                    dot = """<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"> """
                    for _ in range(int(contendio)):
                        dot += repo.imprimirBloques(cont)
                        cont += 64+64
                    dot += """</TABLE>>"""
                    graficas.rep_BLOQUES(dot)
                    print("")
                elif name_rep.lower() == "bm_inode":
                    contendio = ""
                    with open("MAINS/Reportes/b_inode.txt","r") as archivo:
                        contendio = archivo.read()
                        print(contendio)
                    print("")
                elif name_rep.lower() == "bm_block":
                    contendio = ""
                    with open("MAINS/Reportes/b_block.txt","r") as archivo:
                        contendio = archivo.read()
                        print(contendio)
                    print("")
                elif name_rep.lower() == "tree":
                    graficas.rep_Tree()
                    print("")
                elif name_rep.lower() == "sb":
                    if e_local == False:
                        repo.repSuperBloque()
                    print("")
                elif name_rep.lower() == "file":
                    print(f"RUTA: {ruta_rep}")
                    name_ruta = os.path.basename(ruta_rep)
                    contendio = ""
                    with open("MAINS/backs/endinodo.txt","r") as archivo:
                        contendio = archivo.read()
                    
                    lista = [name_ruta]
                    contador = 0
                    data_valor = ""
                    for arch_list in lista:
                        # print(arch_list)
                        for _ in range(int(contendio)):
                            # buscarCAT(path, arch_list,contador)
                            admingCA.reporteFILE(path_del_disco,arch_list,contador,path_rep)
                            contador += 128
                        contador = 0
                    

                    print("")
                elif name_rep.lower() == "ls":
                    graficas.rep_LS()
                    print("")
            

        else:
            print("EL Comando REP necesita de un Path")



def p_listaFilesREP(p):
    '''lista_rep : lista_rep atributosSolo_REP
                        | atributosSolo_REP'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_REP(p):
    '''atributosSolo_REP : GUION ID STRING
                         | GUION PATH DIR
                         | GUION NAME STRING
                         | GUION RUTA DIR'''
    p[0] = (p[2], p[3])

def p_comando_pause(p):
    '''comando : PAUSE '''
    print("\nPAUSE . . . ")
    salida_consola("\nPAUSE ...\n")
    delay_seconds = 2
    time.sleep(delay_seconds)

# Manejo de errores sintácticos
def p_error(p):
    if p == None:
        pass
    else:
        print(f"Error de sintaxis: {p}")
        salida_consola(f"Error de sintaxis: {p}")
        

# Construcción del analizador sintáctico
parser = yacc.yacc()

def main_grammar(instruccion):
    # Lectura de comandos desde la entrada estándar
    # while True:
    try:
        # entrada = input("\nIngrese un comando: ")
        entrada = instruccion
        # if entrada.lower() == "exit":
        #     break
        parser.parse(entrada)
    except EOFError:
        # break
        pass

def salida_consola(texto):
    try:
        with open("BackEnd\contenidoTXT\salida_consola.txt","a") as archivo:
                archivo.write(texto)
    except Exception as e: 
        print(str(e))

