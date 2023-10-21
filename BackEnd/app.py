from flask import Flask, render_template, request, redirect, url_for

import main
import admin


app = Flask(__name__, static_folder='static')


# Simulación de datos de usuario
usuarios = {'rol': '1234', 'pan': 'pan'}

def login_users(id, user, password):
    # print(f"login -user={user} -pass={password} -id={id} ")
    # texto_ingreso = f"login -user={user} -pass={password} -id=441{id}"
    with open("BackEnd\Discos\path_del_disco.txt","r") as archivo:
            path_del_disco = archivo.read()
    
    # main.main_grammar(texto_ingreso)
    encontrado, uid, gid = admin.login(path_del_disco,user,password)
    return encontrado


def ejecutar_comandos_individual(texto_ingresado):
    main.main_grammar(texto_ingresado)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    id       = request.form['id']
    
    if username == "root" and password == "123":
        ejecutar_comandos_individual("login -user=root -pass=123 -id=441root")
        return render_template('archivo.html')
    elif username in usuarios and usuarios[username] == password:
        return render_template('login_usr.html')
    elif login_users(id, username, password):
        # print(f"Usuario {username} ha ingresado")
        main.main_grammar(f"login -user={username} -pass={password} -id={id} ")
        return render_template("login_usr.html")
    else:
        mensaje = 'Usuario o contraseña incorrectos.'
    return render_template('index.html', mensaje=mensaje)



@app.route('/logout', methods=['POST'])
def logout():
    main.main_grammar("logout")
    return redirect(url_for('index'))



@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    

    if uploaded_file.filename != '':
        file_content = uploaded_file.read()
        contenido_ejecutar = file_content.decode().replace('\n', '')


        try:
            with open("BackEnd\contenidoTXT\contenido_ejecutar.txt","w") as archivo:
                archivo.write(contenido_ejecutar)
                print(f"contenido de {uploaded_file.filename} escrito en contenido_ejecutar")
        except Exception as e: 
            print(str(e))


        # Procesa el contenido del archivo aquí
        print(f'Contenido del archivo:\n{file_content.decode()}')
        # return f'Archivo subido: {uploaded_file.filename}<br>Contenido:<br><pre>{file_content.decode()}</pre> <button><a href="/" target="_blank">Ir a otra página</a></button>'
        # initial_text = file_content.decode().replace('\n', '<br>').replace(' ', '&nbsp;')
        # initial_text = f'<pre>{file_content.decode()}</pre>'
        return render_template(f'archivo.html', initial_text=file_content.decode())
    else:
        return 'No se ha seleccionado ningún archivo.'
    


@app.route('/ejecutar_comandos', methods=['POST'])
def ejecutar_comandos():
    texto_input1 = request.form['text-input1']
    salida = ""
    texto_input1 = texto_input1.replace("\r","")
    lista_instrucciones = texto_input1.split("\n")
    print(lista_instrucciones)

    print('Texto ingresado a ejecutar:', texto_input1)

    texto = ""
    try:
        with open("BackEnd\contenidoTXT\salida_consola.txt","w") as archivo:
                archivo.write(texto)
    except Exception as e: 
        print(str(e))
        
    if texto_input1 != "":
        try:
            for instruccion in lista_instrucciones:
                main.main_grammar(instruccion)
          
            with open("BackEnd\contenidoTXT\salida_consola.txt","r") as archivo:
                salida = archivo.read()
    
        except Exception as e: 
            print(str(e))

        return render_template(f'archivo.html', salida_consola=salida, initial_text=texto_input1)
    else:
        return 'No se han ingresado comando a ejecutar'


    
    
    # rr = ""
    
    # try:
    #         with open("BackEnd\contenidoTXT\contenido_ejecutar.txt","r") as archivo:
    #             rr = archivo.read()
    #             # print(f"contenido de {uploaded_file.filename} escrito en contenido_ejecutar")
    #         print(rr)
    #         main.main_grammar(rr)
    # except Exception as e: 
    #     print(str(e))
        
    # # instancia = 
    # # main.main_grammar("execute -path=BackEnd\contenidoTXT\contenido_ejecutar.txt")
    # return render_template('cliente.html')

    




if __name__ == '__main__':
    # Especifica la IP y el puerto aquí
    # Por ejemplo, para usar la IP 0.0.0.0 (todas las interfaces) y el puerto 5000:
    app.run(port=3000, host='127.0.1.2', debug=True) #host='0.0.0.0', debug=True

