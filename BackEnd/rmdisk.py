import os

class RmDisk:
    def __init__(self):
        self.path = ''

    def salida_consola(self,texto):
        try:
            with open("BackEnd\contenidoTXT\salida_consola.txt","a") as archivo:
                    archivo.write(texto)
        except Exception as e: 
            print(str(e))

    def remove(self):

        if self.path:
            if self.path.startswith("\"") and self.path.endswith("\""):
                self.path = self.path[1:-1]
            
            try:
                if os.path.isfile(self.path):
                    if not self.path.endswith(".dsk"):
                        print("\t==== El archivo no tiene la extension correcta ====")
                        self.salida_consola("\t==== El archivo no tiene la extension correcta ====\n")
                    
                    # confirmacion = input("\t---- Esta seguro que desea eliminar el disco Y/N: ")
                    confirmacion = 'y'

                    if confirmacion == 'Y' or confirmacion == 'y' or confirmacion == '1':
                        # os.remove(self.path)
                        # 
                        # Verificar si el archivo existe
                        if os.path.exists(self.path):
                            # El archivo existe, intentar eliminarlo
                            try:
                                os.remove(self.path)
                                print(f"El archivo {self.path} ha sido eliminado.")
                                self.salida_consola(f"El archivo {self.path} ha sido eliminado.\n")
                            except OSError as e:
                                print(f"Error al eliminar el archivo {self.path}: {e}")
                                self.salida_consola(f"Error al eliminar el archivo {self.path}: {e}\n")
                        else:
                            # El archivo no existe
                            print(f"El archivo {self.path} no existe y no se puede eliminar.")
                            self.salida_consola(f"El archivo {self.path} no existe y no se puede eliminar.\n")
                        # 
                        print("\t==== Disco eliminado correctamente ====")
                        self.salida_consola("\t==== Disco eliminado correctamente ====\n")
                    else:
                        print("\t==== El Disco no se borro [no se preocupe, todo bien ;) ] ====")
                        self.salida_consola("\t==== El Disco no se borro [no se preocupe, todo bien ;) ] ====\n")

                else:
                    print("\t==== El disco ingresado NO existe ====")
                    self.salida_consola("\t==== El disco ingresado NO existe ====\n")
            
            except Exception as e:
                print("\t==== Error al intentar eliminar el Disco ====")
                self.salida_consola("\t==== Error al intentar eliminar el Disco ====\n")