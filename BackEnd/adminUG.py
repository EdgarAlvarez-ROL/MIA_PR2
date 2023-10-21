# creador del users.txt

import os

class SalirDeBucles(Exception):
    pass

def login(user, password):
    # Obtener la ruta al archivo en carpeta2 desde la ubicación actual (carpeta1)
    # archivo_path = os.path.join(os.pardir, 'TXTS', 'users.txt')
    # archivo_path = archivo_path.replace('\\','/')

    # Ahora puedes abrir el archivo y trabajar con él
    with open('TXTS/users.txt', 'r') as archivo:
        contenido = archivo.read()

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
    encontrado = False
    uid = -1
    gid = -1
    for i in range(len(cola)):
        for x in range(len(cola[i])):
            if len(cola[i]) > 4:
                # print( cola[i][x])
                if cola[i][x] == user and cola[i][x+1] == password:
                    # print(user)
                    # print(password)
                    encontrado = True
                    uid = int(cola[i][0])
                    gid = buscarGrupoYDevolver(cola[i][2])
                    break
    return encontrado, uid, gid

def buscarGrupoYDevolver(grupo):
    indice = 0
    with open('TXTS/users.txt', 'r') as archivo:
        contenido = archivo.read()
        archivo.close()

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


def crearGrupo(name):
    indice = 0
    with open('TXTS/users.txt', 'r') as archivo:
        contenido = archivo.read()
        archivo.close()

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
                    if cola[i][2] == name:
                        print(f"El Grupo Ingresado: - {name} - ya Existe")
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

    if e_ar:
        # Abre un archivo en modo escritura ('w' significa write)
        archivo = open('TXTS/users.txt', 'a')

        # Escribe contenido en el archivo
        archivo.write(data)

        # Cierra el archivo después de escribir
        archivo.close()
        print(f"Grupo {name} registrado correctamente")


def eliminarGrupo(name):
    with open('TXTS/users.txt', 'r') as archivo:
        contenido = archivo.read()
        archivo.close()
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
        # Abre un archivo en modo escritura ('w' significa write)
        archivo = open('TXTS/users.txt', 'w')

        # Escribe contenido en el archivo
        archivo.write(cont_temp[:-1])

        # Cierra el archivo después de escribir
        archivo.close()
        print(f"Grupo {name} Eliminado correctamente")
    else:
        print("Grupon Ingresado no Existente")





def mkusr(user, password, grp):
    indice = 0
    with open('TXTS/users.txt', 'r') as archivo:
        contenido = archivo.read()
        archivo.close()

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
    print(data)
    
    # print(grp_bool)
    if e_ar and grp_bool:
        # Abre un archivo en modo escritura ('w' significa write)
        archivo = open('TXTS/users.txt', 'a')

        # Escribe contenido en el archivo
        archivo.write(data)

        # Cierra el archivo después de escribir
        archivo.close()
        print(f"Usuario {user} registrado correctamente")



def rmuser(user):
    with open('TXTS/users.txt', 'r') as archivo:
        contenido = archivo.read()
        archivo.close()
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
        # Abre un archivo en modo escritura ('w' significa write)
        archivo = open('TXTS/users.txt', 'w')

        # Escribe contenido en el archivo
        archivo.write(cont_temp[:-1])

        # Cierra el archivo después de escribir
        archivo.close()
        print(f"Usuario {user} Eliminado correctamente")
    else:
        print("Usurio Ingresado no Existente")

# estado = login("root","123")
# print(estado)

# crearGrupo("hola")
# crearGrupo("estudiantes")
# crearGrupo("usuarios")
# eliminarGrupo("usuarios")

# mkusr("paladin2","83afa","usuarios")
# rmuser("paladin")

# encontrado, uid, gid = login("uno","uno")
# print(f"encontrado: {encontrado}, uid: {uid}, gid: {gid}")