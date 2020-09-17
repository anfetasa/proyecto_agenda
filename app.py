from flask import Flask, render_template, request, redirect, url_for, flash, session, escape, logging
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt


#configuracion basica y de cookies
app = Flask(__name__)
app.secret_key = "my_secret_key"


#configuracion de la base de datos y la coneccion a la misma

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'anfetasa'
app.config['MYSQL_PASSWORD'] = 'qawsed123'
app.config['MYSQL_DB'] = 'proyecto_agenda'

mysql = MySQL(app)

#el siguiente bloque de codigo fue realizado por Andres Taborda

#ruta principal que renderiza el template html del formulario de inicio de sesion

@app.route('/')
def index():

    return render_template('login.html')

#ruta que renderiza el template html del formulario de registro de usuario

@app.route('/registrarse')
def registrarse():
    return render_template('registro.html')

#ruta para agregar un usuario

@app.route('/add_user', methods=['POST' ,'GET'])
def add_user():

    #aca se reciben todos los datos otorgados en el formulario html
    
    if request.method =='POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        confirmar_pass = request.form['confirmar_pass']
        
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM usuarios WHERE correo= '%s'" % correo)
        print(result)
        print(nombre)

        #se hace una validacion de que las contraseñas coincidan y que no exista el usuario

        if contraseña == confirmar_pass and result == 0:
            cur.execute('INSERT INTO usuarios (nombre, correo, contraseña) VALUES (%s,%s,%s)', (nombre, correo, contraseña))

            mysql.connection.commit()
            #El comando flash almacena el mensaje que sobrepone en pantalla y se imprime en el html
            flash('Usuario agregado satisfactoriamente')
            return redirect(url_for('registrarse'))

        else:
            flash('Error al registrar un usuario')

            return redirect(url_for('registrarse'))

#Validacion para ingresar / iniciar sesion

@app.route('/inicio', methods=['POST' ,'GET'])

def inicio():

    #recuperar los datos del formulario de inicio de sesion

    if request.method =='POST':
        usuario = request.form['user']
    
        contrasena = request.form['password']

        cur = mysql.connection.cursor()

        #hacer una validacion de que el correio (usuario) y la contraseña existan

        result = cur.execute("SELECT correo, contraseña FROM usuarios WHERE correo= '%s' and contraseña = '%s'" % (usuario, contrasena))

        if result > 0 :

            #Sacar de la base de datos el id del usuario

            cur.execute("SELECT idusuarios FROM usuarios WHERE correo= '%s' and contraseña = '%s'" % (usuario, contrasena))
            
            idUsuarios = cur.fetchone()

            for i in idUsuarios:
                idUsuario = i
                
        
            #Guardar el id, usuario, la contraseña y confirmar que inicio sesion en  las cookies del navegador
            session['id'] = idUsuario
            session['logged_in'] = True
            session['username'] = usuario
            session['password'] = contrasena

            #retorna a la pagina principal de la aplicacion donde se ven los eventos de la agenda
            return redirect(url_for('home'))

        else:
            
            #retorna un error
            flash ("Error al iniciar sesion")
            return redirect(url_for('index'))
          
#Ruta donde se vizualizaran los eventos programados

@app.route('/home')
def home():

    #se hace una validacion de que este iniciada sesion con ayuda de las cookies
    
    if session['logged_in'] == True:
        
        return redirect(url_for('eventos'))

    #Si no ha iniciado sesion lo redirige al formulario de inicio de sesion
    else:
        return redirect(url_for('index'))

#ruta para rederizar el perfil.html

@app.route('/ver_perfil')
def verPerfil():

    #validacion de que se encuentre con la sesion iniciada

    if session['logged_in'] == True:
        
        idUsuario = session['id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE idusuarios= '%s'" % idUsuario)
        data = cur.fetchall()
        return render_template('perfil.html', usuarios = data)

    else:
        flash('Error, no ha iniciado sesion')

        return redirect(url_for('index'))

#ruta para renderizar la parte de editar pefil

@app.route('/editar_perfil')
def editarPerfil():

    #validacion de que se encuentre con la sesion iniciada

    if session['logged_in'] == True:
      
        idUsuario = session['id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE idusuarios =%s" % idUsuario)
        data = cur.fetchall()
        return render_template('editarPerfil.html', usuarios = data[0])
    else:
        return "Error al iniciar sesion"

#metodo para editar el perfil de la base de datos

@app.route('/actualizar_perfil', methods=['POST' ,'GET'])

def actualizar():
    #se extrae la nueva informacion del formulario
    if request.method =='POST':
        idUsuario = session['id']
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        str(idUsuario)
        
        correo2 = session['username']
        cur = mysql.connection.cursor()

        #validaciones de que si va a modificar su usuario, el usuario no exista en la base de datos
        if correo2 == correo:
        #se actualiza en la base de datos
            cur.execute("UPDATE usuarios SET nombre= %s, correo = %s, contraseña= %s WHERE idusuarios =%s" , (nombre, correo, contraseña, idUsuario))

            #se confirma la actualizacion

            mysql.connection.commit()

            flash('Actualizado correctamente')
    
            return redirect(url_for('verPerfil'))

        else: 
            result = cur.execute("SELECT * FROM usuarios WHERE correo= '%s'" % correo)
            if result == 0:
                cur.execute("UPDATE usuarios SET nombre= %s, correo = %s, contraseña= %s WHERE idusuarios =%s" , (nombre, correo, contraseña, idUsuario))

                #se confirma la actualizacion

                mysql.connection.commit()

                flash('Actualizado correctamente')
        
                return redirect(url_for('verPerfil'))
            else: 
                flash('Usuario ya registrado')

                return redirect(url_for('verPerfil'))

#metodo para cerrar sesion

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('logged_in', None)
    session.pop('username', None) 
    session.pop('password', None)
    session.pop('id', None)

    return redirect(url_for('index'))

#fin bloque de codigo de andres

#el siguiente bloque de codigo fue realizado por sebatian rodriguez

#ruta que rederiza la seccion donde se visualizan los eventos
@app.route("/eventos")
def eventos():
    if session['logged_in'] == True:
        idUsuario = session['id']
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM eventos WHERE idUsuario = %s" % idUsuario)
        data = con.fetchall()
        return render_template("index.html", data=data)
    else:
        return "Primero inicie sesion"

#ruta para agregar un nuevo evento
@app.route('/agregar', methods=['POST'])
def agregar():
    if session['logged_in'] == True:
        if request.method == 'POST':
            idUsuario = session['id']
            titulo = request.form['titulo']
            hora = request.form['hora']
            fecha = request.form['fecha']
            descripcion = request.form['descripcion']
            con = mysql.connection.cursor()
            con.execute("INSERT INTO eventos (titulo,hora,dia,descripcion,idUsuario) VALUES (%s,%s,%s,%s,%s)",
                        (titulo, hora, fecha, descripcion, idUsuario))
            mysql.connection.commit()
            return redirect(url_for("eventos"))
    else: 
        return "Primero inicie sesion"

#ruta para eliminar un evento
@app.route("/borrar/<string:id>")
def borrar(id):
    if session['logged_in'] == True:
        con = mysql.connection.cursor()
        con.execute("DELETE FROM eventos WHERE id = {0}".format(id))
        mysql.connection.commit()
        return redirect(url_for("eventos"))
    else: 
        return "Primero inice sesion"

#ruta para modificar un evento y renderizar el formulario
@app.route('/cambiar/<id>', methods=['POST', 'GET'])
def cambiar(id):
    if session['logged_in'] == True:
        con = mysql.connection.cursor()
        con.execute('SELECT * FROM eventos WHERE id = %s', (id,))
        data = con.fetchall()
        con.close()
        return render_template('change.html', data=data)
    return "Primero inicie sesion"

#ruta en la que se confirma que modifica un evento
@app.route("/cambiarc/<id>", methods=['POST'])
def cambiarc(id):
    if session['logged_in'] == True:
        if request.method == 'POST':
            titulo = request.form['titulo']
            hora = request.form['hora']
            fecha = request.form['fecha']
            descripcion = request.form['descripcion']
            con = mysql.connection.cursor()
            con.execute("""
                UPDATE eventos SET titulo = %s, hora = %s, dia = %s, descripcion = %s WHERE id = %s """, (titulo, hora, fecha, descripcion, id,))
            mysql.connection.commit()
            return redirect(url_for('eventos'))
    return "Primero inicie sesion"
#Fin bloque de codigo de sebatian



if __name__ == '__main__':
    app.run(port= 3000, debug= True)







