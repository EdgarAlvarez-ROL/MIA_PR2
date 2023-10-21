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
    'STRING',
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

def t_FILE1(t):
    r'file[0-9]'
    return t

def t_FILE2(t):
    r'file[0-9][0-9]*'

# Expresión regular para directorio
def t_DIR(t):
    # r'\/[a-zA-Z0-9_\/\.]+ | \"\/[a-zA-Z0-9_\/\.]+\"'

    # r'C:\\[^\\]+(\\[^\\]+)*\\[^.]+\.dsk | \"C:\\[^\\]+(\\[^\\]+)*\\[^.]+\.dsk\"'

    r'C:\\[^\\]+(\\[^\\]+)*\\[^.]+\.[a-zA-Z0-9]+ | \"C:\\[^\\]+(\\[^\\]+)*\\[^.]+\.[a-zA-Z0-9]+\"'
    if t.value.startswith('"') or t.value.startswith("'"):
        t.value = t.value[1:-1]  # Eliminar las comillas alrededor de la cadena

    # r'[^\\]+(\\[^\\]+)*\\[^.]+\.[a-zA-Z0-9]+'
    # r'\\[a-zA-Z0-9_\\\.]+'
    return t

# def t_STRING(t):
#     r'=(\"[^\"]*\") | =([a-zA-Z0-9_]+[a-zA-Z0-9]*)'
#     if t.value.startswith('"') or t.value.startswith("'"):
#         t.value = t.value[1:-1]  # Eliminar las comillas alrededor de la cadena
#     return t


# Expresiones regulares de cadena para que no entre en conflico con los tokens simples
def t_CADENA(t):
    r'(\"[^"]*\"|\'[^\']*\')'
    if t.value.startswith('"') or t.value.startswith("'"):
        t.value = t.value[1:-1]  # Eliminar las comillas alrededor de la cadena
    # Verifica si la cadena es una palabra clave
    # t.type = reserved.get(t.value, 'CADENA')
    return t

def t_NUMERO(t):
    r'\d+'  # Reconoce secuencias de dígitos como números
    t.type = 'NUM'
    t.value = int(t.value)  # Convierte la cadena a un entero
    return t

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

path_del_disco = ""
bandera_mkfile = False
pp = -1
block_start = -1

first = True


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

    # imprimir valores ingresados
    print("Size: "+str(size))
    print("Unit: "+str(unit))
    print("Fit: "+str(fit))
    print("Path: "+str(path))
    
    path_del_disco = path
    # creacion del disco con los valores ingresados
    disk = MkDisk()
    disk.path = path
    disk.size = size
    disk.unit = unit
    disk.fit = fit
    disk.create()

    # reseteo de las variables para su uso futuro
    size = ""
    unit = ""
    path_del_disco = path
    # mkdisk -size=5 -unit=M -path=C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\DISCOS\disco.dsk
    

def p_atributosM(p):
    '''atributosm : atributosm atributom
                 | atributom'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoM(p):
    '''atributom : GUION PATH IGUAL DIR
                 | GUION FIT IGUAL LETRAS_FIT
                 | GUION UNIT IGUAL LETRA_FDISK
                 | GUION SIZE IGUAL NUM'''
    p[0] = (p[2], p[4])



# Reglas para el comando fdisk
def p_comando_fdisk(p):
    '''comando : FDISK atributos'''
    global command, size, unit_fkdisk, path, name, type, fit, add
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

        partition = FDisk()
        partition.delete = delete
        partition.size = size
        partition.type = type
        partition.unit = unit_fkdisk
        partition.path = path
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


def p_atributos(p):
    '''atributos : atributos atributo
                 | atributo'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributo(p):
    '''atributo : GUION PATH IGUAL DIR
                | GUION TYPE IGUAL LETRA_FDISK
                | GUION UNIT IGUAL LETRA_FDISK
                | GUION NAME IGUAL CADENA
                | GUION SIZE IGUAL NUM
                | GUION FIT IGUAL LETRAS_FIT
                | GUION ADD IGUAL NUM
                | GUION DELETE'''
    p[0] = (p[2], p[4])



# reglas comadno REP
def p_comando_rep(p):
    '''comando : REP GUION PATH IGUAL DIR'''
    global path
    
    path = p[5]
    # Eliminando las comillas del path
    if path.startswith("\""):
        path = path[1:-1]

    repo = reporte()
    repo.path = path
    repo.rep()


def p_comando_rmdisk(p):
    '''comando : RMDISK GUION PATH IGUAL DIR'''
    global path

    path = p[5]
    # Eliminando las comillas del path
    if path.startswith("\""):
        path = path[1:-1]

    print(f"Ruta del archivo a eliminar: {path}")
    rm = RmDisk()
    rm.path = path
    rm.remove()


def p_comando_mount(p):
    '''comando : MOUNT atributos_mount'''
    global numParticion, path_mount, name_mount, mount
    # MONTA UNA PARTICION DEL DISCO, como: saber?
    # inicioParticion = "44"
    command = "mount"
    print(f"Comando: {command}")
    for atributo in p[2]:
        if atributo[0] == "path":
            path_mount = atributo[1] 
        elif atributo[0] == "name":
            name_mount = atributo[1]
    
    if name_mount == "" or path_mount == "":
        print("Se necesita el path y el name para ejecutar el comando Mount")
    else:
        print("Path: "+str(path_mount))
        print("Name de la particion a usar: "+str(name_mount))
        mount(path_mount, name_mount)
        mount.listaMount()

    


def p_atributos_mount(p):
    '''atributos_mount : atributos_mount atributo_mm
                 | atributo_mm'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributo_mount(p):
    '''atributo_mm : GUION PATH IGUAL DIR
                   | GUION NAME IGUAL CADENA'''
    p[0] = (p[2], p[4])



def p_comando_unmount(p):
    '''comando : UNMOUNT GUION ID IGUAL CADENA'''
    global path_mount, name_mount, mount
    # id = ""
    command = "unmount"
    print(f"Comando: {command}")
    id = p[5]
    print(f"ID: {id}")
    mount.unmount(id)
    


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

        fileSystem = MKFS(mount)
        tks = [id,type,fs_val]
        fileSystem.mkfs(tks)
    else: 
        print("El comando MKFS requiere obligatoriamente de un id")


def p_atributos_mkfs(p):
    '''atributos_mkfs : atributos_mkfs atributosSolo_mkfs
                        | atributosSolo_mkfs'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_mkfs(p):
    '''atributosSolo_mkfs : GUION ID IGUAL NAME
                            | GUION TYPE IGUAL CADENA
                            | GUION FS IGUAL FS_VAL'''
    p[0] = (p[2], p[4])



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
            # print("mandamos la data a la particion con el id")

        else:
            print("Usuario NO encontrado")
    else:
        print("Porfavor ingrese todos los datos del user, password, id\n")


def p_atributos_login(p):
    '''atributos_login : atributos_login atributosSolo_login
                        | atributosSolo_login'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributoSolo_login(p):
    '''atributosSolo_login :  GUION USER IGUAL CADENA
                            | GUION PASS IGUAL CADENA
                            | GUION ID IGUAL CADENA'''
    p[0] = (p[2], p[4])


# SALE DE LA SESION
def p_comando_logout(p):
    '''comando : LOGOUT'''
    global user, id, password
    print(f"SALIENDO de la Sesion {user} ...")
    user = ""
    id = ""
    password = ""


# ESCRIBE un grupo en el users.txt 
# solo lo puede usar el ROOT
def p_comando_mkgrp(p):
    '''comando : MKGRP GUION NAME IGUAL CADENA'''
    global sesion_Iniciada, user, path_del_disco
    name = p[5]
    if user == "root" or user == "ROOT":
        if sesion_Iniciada:
            print("Comando: MKGRP usuario ROOT")
            admin.mkgrp(path_del_disco, name)
        else:
            print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
    else:
        print("Solo el usuario ROOT con su sesion iniciada puede ejecutar este comando")
        print("Porfavor INICIE SESION como ROOT para ejecutar este comando")


def p_comando_rmgrp(p):
    '''comando : RMGRP GUION NAME IGUAL CADENA'''
    global sesion_Iniciada, user, path_del_disco
    name = p[5]
    if user == "root" or user == "ROOT":
        if sesion_Iniciada:
            print("Comando: RMGRP usuario ROOT")
            admin.rmgrp(path_del_disco,name)
            # adminUG.eliminarGrupo(name)
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
            print("Comando: RMGRP usuario ROOT")
            # adminUG.mkusr(name_ingresar,pass_ingresar,grp)
            admin.mkusr(path_del_disco,name_ingresar,pass_ingresar,grp)
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
    '''atributosSolo_mkusr :  GUION USER IGUAL CADENA
                            | GUION PASS IGUAL CADENA
                            | GUION GRP IGUAL CADENA'''
    p[0] = (p[2], p[4])




def p_comando_rmusr(p):
    '''comando : RMUSR GUION NAME IGUAL CADENA'''
    global sesion_Iniciada, user, sesion_Iniciada, path_del_disco
    name_ingresar = p[5]
    

    if user == "root" or user == "ROOT":
        if sesion_Iniciada:
            print("Comando: RMUSR usuario ROOT")
            # adminUG.rmuser(name_ingresar)
            admin.rmusr(path_del_disco,name_ingresar)
        else:
            print("Porfavor INICIE SESION como ROOT para ejecutar este comando")
    else:
        print("Solo el usuario ROOT con su sesion iniciada puede ejecutar este comando")
        print("Porfavor INICIE SESION como ROOT para ejecutar este comando")






# MKFILE
def p_comando_mkfile(p):
    '''comando : MKFILE atributos_mkfile'''
    global permiso_Usuario, user, sesion_Iniciada, bandera_mkfile, pp, block_start, path_del_disco
    
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

            if size_mkfile == "":
                size_mkfile = "0"

            if path_mkfile == "":
                print("Porfavor Ingrese el Path Obligatorio del comando MKFILE")
            elif int(size_mkfile) < 0:
                print("No se aceptan numeros negativos en size")
            else:
                print("Ejecutando...")
                # print("Comando MKFILE")
                caracteres_escritos = 0
                cont = 0
                secuencia = "0123456789"
                relleno_archivo = ""
                while caracteres_escritos < size_mkfile:
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
                first = False
    

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
    '''atributosSolo_mkfile : GUION PATH IGUAL DIR
                            | GUION SIZE IGUAL NUM
                            | GUION CONT IGUAL CADENA
                            | GUION R'''
    if len(p) == 3:
        p[0] = (p[2], p[1])
    else:
        p[0] = (p[2], p[4])

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
    path_del_disco = r"C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\DISCOS\disco.dsk"
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

def p_atributoSolo_CAT(p):
    '''atributosSolo_CAT : GUION FILE2 IGUAL DIR
                         | GUION FILE1 IGUAL DIR'''
    p[0] = (p[2], p[4])

#  =======================================================================================================



# REMOVE
def p_comando_remove(p):
    '''comando : REMOVE GUION PATH IGUAL DIR'''
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
    '''atributosSolo_EDIT : GUION PATH IGUAL DIR
                         |  GUION CONT IGUAL DIR'''
    p[0] = (p[2], p[4])



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
    '''atributosSolo_RENAME : GUION PATH IGUAL DIR
                            | GUION NAME IGUAL CADENA'''
    p[0] = (p[2], p[4])



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
    '''atributosSolo_MKDIR : GUION PATH IGUAL DIR
                           | GUION R'''
    if len(p) == 3:
        p[0] = (p[2], p[1])
    else:
        p[0] = (p[2], p[4])



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
    '''atributosSolo_COPY : GUION PATH IGUAL DIR
                          | GUION DESTINO IGUAL DIR'''

    p[0] = (p[2], p[4])



def p_comando_execute(p):
    """comando : EXECUTE GUION PATH IGUAL DIR"""
    print("HOLA")

# Manejo de errores sintácticos
def p_error(p):
    print(f"Error de sintaxis: {p}")

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Lectura de comandos desde la entrada estándar
while True:
    try:
        entrada = input("\nIngrese un comando: ")
        if entrada.lower() == "exit":
            break
        parser.parse(entrada)
    except EOFError:
        break
