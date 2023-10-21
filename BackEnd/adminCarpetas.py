import os
import shutil


def crearArchivo(path_del_disco,path,size,r,cont,usuario,permisos,uid,gid,bandera_mkfile,newPP,newBLOCKStart):
    import WR
    # Tamaño en caracteres deseado
    tamano_caracteres = size  # Cambia este valor al tamaño deseado en caracteres

    
    # Secuencia de números del 0 al 9 en forma de cadena
    secuencia = "0123456789"
    contenido = ""

    if r:
        crear_carpetas_si_no_existen(path)
    
    if cont != "":
        with open(cont, "r") as archivo2:
            contenido = archivo2.read()
            # print(contenido)
            archivo2.close()

        with open(path, "w") as archivo:
            archivo.write(contenido)
            archivo.close()
    else:
        try:
            # Abre un archivo de texto en modo escritura
            with open(path, "w") as archivo:
                caracteres_escritos = 0
                cont = 0
                while caracteres_escritos < tamano_caracteres:
                        if cont > 9:
                            cont = 0
                        archivo.write(secuencia[cont])
                        caracteres_escritos += 1
                        cont += 1
            print(f"Se ha creado el archivo de texto con {tamano_caracteres} bytes que contiene la secuencia de números del 0 al 9.")
        except Exception as e:
            print(f"Error las carpetas que preceden al archivo no existen {path}: {str(e)}")
        
        
        # SECCION DEL BLOQUE ARCHIVO E INODO
        archivo = 1
        pp = -1
        block = -1
        if bandera_mkfile:
            aa, bb = WR.mkfileInodo(path_del_disco,path,usuario,permisos,archivo,uid,gid,newPP,newBLOCKStart)
        else:
            aa, bb = WR.mkfileInodo(path_del_disco,path,usuario,permisos,archivo,uid,gid,"","")
        pp = aa
        block = bb
        
        return pp, block
        """"""


def crear_carpetas_si_no_existen(path):
    # path = path.replace("\\","/")
    nombre_archivo = os.path.basename(path)
    # print(nombre_archivo)
    path = path.replace(nombre_archivo, "")
    # print(path[:-1])
    try:
        # Intentar crear las carpetas si no existen
        os.makedirs(path)
        print(f"Carpetas creadas en: {path[:-1]}")
    except FileExistsError:
        print(f"Las carpetas ya existen en: {path}")
    except Exception as e:
        print(f"Error al crear carpetas en {path}: {str(e)}")

# # Ingresa la ruta que deseas y llama a la función
# ruta_deseada = "Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\GSS\EXE\IN.txt"
# crear_carpetas_si_no_existen(ruta_deseada)

def otro(carpeta):
    # carpeta = carpeta.replace("\\","\\\\")
    print(carpeta)
    for archivo in os.listdir(carpeta):
        print(archivo)


def cat(lista):
    for data in lista:
        path = data[1]

        # print(path)

        with open(path, "r") as archivo2:
                contenido = archivo2.read()
                # print(contenido)
                archivo2.close()
        
        print(contenido)


def remover(path):
    ruta = path

    nombre_archivo = os.path.basename(ruta)
    # print("Nombre del archivo:", nombre_archivo)
    if "." in nombre_archivo:
        print("Nombre del archivo a REMOVER:", nombre_archivo)
        archivo_a_eliminar = path  # Reemplaza esto con el nombre del archivo que deseas eliminar
        try:
            os.remove(archivo_a_eliminar)
            print(f"El archivo '{archivo_a_eliminar}' ha sido eliminado correctamente.")
        except FileNotFoundError:
            print(f"El archivo '{archivo_a_eliminar}' no existe.")
        except Exception as e:
            print(f"Ocurrió un error al eliminar el archivo: {str(e)}")

    else:
        carpeta_a_eliminar = path  # Reemplaza esto con el nombre de la carpeta que deseas eliminar

        try:
            shutil.rmtree(carpeta_a_eliminar)
            print(f"La carpeta '{carpeta_a_eliminar}' y su contenido han sido eliminados correctamente.")
        except FileNotFoundError:
            print(f"La carpeta '{carpeta_a_eliminar}' no existe.")
        except OSError as e:
            print(f"Ocurrió un error al eliminar la carpeta y su contenido: {str(e)}")



def edit(path, cont):

    nombre_archivo = cont  # Reemplaza con el nombre del archivo que deseas leer
    contenido = ""
    try:
        with open(nombre_archivo, "r") as archivo:
            contenido = archivo.read()
        print("Contenido del archivo CONT:")
        print(contenido)
    except FileNotFoundError:
        print(f"El archivo en '{nombre_archivo}' no existe.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {str(e)}")


    nombre_archivo = path  # Reemplaza con el nombre del archivo en el que deseas escribir

    try:
        with open(nombre_archivo, "w") as archivo:
            datos_a_escribir = contenido
            archivo.write(datos_a_escribir)
        print(f"Los datos se han escrito correctamente en el archivo '{nombre_archivo}'.")
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no existe.")
    except Exception as e:
        print(f"Ocurrió un error al escribir en el archivo: {str(e)}")


def rename(path, name):
    ruta_actual = path 
    nuevo_nombre = name 

    try:
        os.rename(ruta_actual, nuevo_nombre)
        print(f"El archivo o carpeta '{ruta_actual}' se ha renombrado como '{nuevo_nombre}' correctamente.")
    except FileNotFoundError:
        print(f"El archivo o carpeta '{ruta_actual}' no existe.")
    except Exception as e:
        print(f"Ocurrió un error al renombrar el archivo o carpeta: {str(e)}")


def mkdir(path, r):
    if r:
        path += r"\borrar.txt"
        crear_carpetas_si_no_existen(path)
        path = path[:-10]
        print(path)

    try:
        # Intentar crear las carpetas si no existen
        os.makedirs(path)
        print(f"Carpetas creadas en: {path}")
    except FileExistsError:
        print(f"Las carpetas ya existen en: {path}")
    except Exception as e:
        print(f"Error al crear carpetas en {path}: {str(e)}")




def copy(path, destino):
    archivo = False
    if "." in (os.path.basename(path)):
        archivo = True
    
    if archivo:
        """Copia de Archivo"""
        archivo_origen = path # Reemplaza con la ruta del archivo que deseas copiar
        archivo_destino = destino  # Reemplaza con la ruta donde deseas copiar el archivo

        try:
            os.chmod(archivo_destino, 0o755)
            shutil.copy(archivo_origen, archivo_destino)
            print(f"El archivo '{os.path.basename(archivo_origen)}' se ha copiado correctamente a '{archivo_destino}'.")
        except FileNotFoundError:
            print(f"El archivo '{archivo_origen}' no existe.")
        except Exception as e:
            print(f"Ocurrió un error al copiar el archivo: {str(e)}")

    else:
        """Copia de Carpeta"""
        directorio_origen = path  # Reemplaza con la ruta del directorio que deseas copiar
        directorio_destino = destino  # Reemplaza con la ruta donde deseas copiar el directorio

        try:
            # os.chmod(directorio_destino, 0o777)
            shutil.copy(directorio_origen, directorio_destino)
            print(f"El directorio '{directorio_origen}' y su contenido se han copiado correctamente a '{directorio_destino}'.")
        except FileNotFoundError:
            print(f"El directorio '{directorio_origen}' no existe.")
        except Exception as e:
            print(f"Ocurrió un error al copiar el directorio y su contenido: {str(e)}")


# mkdir(r"C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\G\SOL\uno",False)


# path = r"C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\G\cua\adfafd.txt"
# cont = r"C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\G\hola to.txt"
# edit(path,cont)


# remover(r"C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\G\cua")

# crearArchivo(r"C:\Users\wwwed\OneDrive\Escritorio\Octavo_Semestre\LAB_Archivos\MIA_T2_202001144\T2\G\sxaa.txt",13,True,"")
# otro(r"C:\Users\wwwed\OneDrive\Escritorio\pruebas_todoTipo\Organizers")

# lista = [1,0,0,1,5,8,8]
# cat(lista)


