
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
    session['logged_in'] = False
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

    if session['logged_in'] == True :
        
        return redirect(url_for('eventos'))

    #Si no ha iniciado sesion lo redirige al formulario de inicio de sesion
    else:
        flash ("Primero inicie sesion")
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
        flash ("Primero inicie sesion")
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
        flash ("Primero inicie sesion")
        return redirect(url_for('index'))

#metodo para editar el perfil de la base de datos

@app.route('/actualizar_perfil', methods=['POST' ,'GET'])

def actualizar():
    if session['logged_in'] == True:
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
    else:
        flash ("Primero inicie sesion")
        return redirect(url_for('index'))

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
    if session['logged_in'] == True :
        idUsuario = session['id']
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM eventos WHERE idLider=%s OR idUsuario= %s", (idUsuario, idUsuario))
        data = con.fetchall()
        return render_template("index.html", data=data, idUsuario = idUsuario)
    else:
        flash ("Primero inicie sesion")
        return redirect(url_for('index'))

#ruta para agregar un nuevo evento
@app.route ("/nuevoEvento")
def nuevoEvento():
    if session['logged_in'] == True :
          return render_template("nuevoEvento.html")
    else:
        flash ("Primero inicie sesion")
        return redirect(url_for('index'))

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
            con.execute("INSERT INTO eventos (titulo,hora,dia,descripcion,idUsuario) VALUES (%s,%s,%s,%s,%s)", (titulo, hora, fecha, descripcion, idUsuario))
            mysql.connection.commit()
            flash ("Evento agregado satisfactoriamente")
            return redirect(url_for("eventos"))
    else:
        flash ("Primero inicie sesion")
        return redirect(url_for('index'))

#ruta para eliminar un evento
@app.route("/borrar/<string:id>/<string:titulo>/<string:hora>/<string:dia>/<string:descripcion>")
def borrar(id, titulo, hora, dia, descripcion):
    if session['logged_in'] == True:
        idUsuario = session['id']
        con = mysql.connection.cursor()
        titulo1= "{0}".format(titulo)
        hora1= "{0}".format(hora)
        dia1= "{0}".format(dia)
        descripcion1= "{0}".format(descripcion)
        query = con.execute("SELECT * FROM eventos WHERE idLider = %s AND titulo  = %s AND hora  = %s AND dia  = %s AND descripcion  = %s" , (idUsuario, titulo1, hora1, dia1, descripcion1))
        if query == 0:
            con.execute("DELETE FROM eventos WHERE id = {0}".format(id))
            mysql.connection.commit()
        elif query >= 1:
            con.execute("DELETE FROM eventos WHERE idLider = %s AND titulo  = %s AND hora  = %s AND dia  = %s AND descripcion  = %s" , (idUsuario, titulo1, hora1, dia1, descripcion1))
            mysql.connection.commit()
        flash ("Eliminado satisfactoriamente")
        return redirect(url_for("eventos"))
    else:
        flash ("Primero inicie sesion")
        return redirect(url_for('index'))

#ruta para modificar un evento y renderizar el formulario
@app.route('/cambiar/<string:id>/<string:titulo>/<string:hora>/<string:dia>/<string:descripcion>', methods=['POST', 'GET'])
def cambiar(id, titulo, hora, dia, descripcion):
    if session['logged_in'] == True :
        idUsuario = session['id']
        con = mysql.connection.cursor()
        con.execute('SELECT * FROM eventos WHERE id = %s', (id,))
        data = con.fetchall()
        con.close()

        return render_template('change.html', data=data)

    else:
        flash ("Primero inicie sesion")
        return redirect(url_for('index'))

#ruta en la que se confirma que modifica un evento
@app.route("/cambiarc/<string:id>/<string:titulo>/<string:hora>/<string:dia>/<string:descripcion>", methods=['POST'])
def cambiarc(id, titulo, hora, dia, descripcion):
    if session['logged_in'] == True:
        if request.method == 'POST':
            idUsuario = session['id']
            titulo2 = request.form['titulo']
            hora2 = request.form['hora']
            fecha2 = request.form['fecha']
            descripcion2 = request.form['descripcion']
            con = mysql.connection.cursor()
            titulo1= "{0}".format(titulo)
            hora1= "{0}".format(hora)
            dia1= "{0}".format(dia)
            descripcion1= "{0}".format(descripcion)
            query = con.execute("SELECT * FROM eventos WHERE idLider = %s AND titulo  = %s AND hora  = %s AND dia  = %s AND descripcion  = %s" , (idUsuario, titulo1, hora1, dia1, descripcion1))
            if query == 0:
                con.execute("""
                    UPDATE eventos SET titulo = %s, hora = %s, dia = %s, descripcion = %s WHERE id = %s """, (titulo2, hora2, fecha2, descripcion2, id,))
                mysql.connection.commit()
            elif query >= 1:
                con.execute("""
                    UPDATE eventos SET titulo = %s, hora = %s, dia = %s, descripcion = %s WHERE idLider = %s AND titulo  = %s AND hora  = %s AND dia  = %s AND descripcion  = %s """, (titulo2, hora2, fecha2, descripcion2, idUsuario, titulo1, hora1, dia1, descripcion1))
                mysql.connection.commit()
            flash ("Actualizado satisfactoriamente")
            return redirect(url_for('eventos'))
    else:
        flash ("Primero inicie sesion")
        return redirect(url_for('index'))
#Fin bloque de codigo de sebatian

#Inicio bloque de codigo de andres

#Ruta para crear eventos grupales
@app.route("/eventoGrupal", methods=['POST', 'GET'])
def eventoGrupal():
    idGrupo = []
    idGrupo2 = []
    usuarioNoEncontrado = []
    if session['logged_in'] == True:
        idUsuario = session['id']
        if request.method == 'POST':
            
            #se toman los datos proporcionados por el creador del evento grupal y se almacenan en la base de datos
            usuarios = request.form['usuarios']
            listaUsuarios = usuarios.split(";")
            titulo = request.form['titulo']
            hora = request.form['hora']
            fecha = request.form['fecha']
            descripcion = request.form['descripcion']
            con = mysql.connection.cursor()
            for i in listaUsuarios:
                con.execute("SELECT idUsuarios FROM usuarios Where correo = %s", (i,))
                x = con.fetchone()
                if x != None:
                    idGrupo.append(x)
                else:
                   usuarioNoEncontrado.append(i)
            for i in idGrupo:
                for x in i:
                    idGrupo2.append(x)
            if len(listaUsuarios) == len(idGrupo2):
                
                con.execute("INSERT INTO eventos (titulo,hora,dia,descripcion,idUsuario, idLider) VALUES (%s,%s,%s,%s,%s, %s)", (titulo, hora, fecha, descripcion, idUsuario, idUsuario))

                mysql.connection.commit()
                print(fecha)

                for i in idGrupo2:
                    con.execute("INSERT INTO eventos (titulo,hora,dia,descripcion,idUsuario, idLider) VALUES (%s,%s,%s,%s,%s, %s)", (titulo, hora, fecha, descripcion, i, idUsuario))
                    mysql.connection.commit()
                flash ("Reunion grupal creada satisfactoriamente")
                return redirect(url_for("eventos"))
            else:
    

                for i in usuarioNoEncontrado:
                    flash('Usuario no encontrado: ' + i)
                    return redirect(url_for('eventoGrupal'))

        return render_template('eventoGrupal.html')
    else:
        flash ("Primero inicie sesion")
        return redirect(url_for('index'))

#Fin bloque de codigo de andres


#Filtar

@app.route("/filetitulo", methods=['POST'])

def filetitulo():
    if request.method == "POST":
        titulo = "%" + request.form['titulo'] + "%"
        con = mysql.connection.cursor()
        con.execute('SELECT * FROM eventos WHERE titulo LIKE %s',(titulo,))
        data = con.fetchall()
        idUsuario = session['id']
        return render_template("index.html", data=data, idUsuario = idUsuario)

@app.route("/filehora", methods=['POST'])

def filehora():
    if request.method == "POST":
        hora = request.form['hora']
        print(hora)
        h = "%H:%i"
        con = mysql.connection.cursor()
        con.execute('SELECT * FROM eventos WHERE DATE_FORMAT(hora, %s )  = %s',(h, hora,))
        data = con.fetchall()
        idUsuario = session['id']
        return render_template("index.html", data=data,idUsuario = idUsuario)

@app.route("/filefecha", methods=['POST'])

def filefecha():
    if request.method == "POST":
        fecha = request.form['fecha']
        con = mysql.connection.cursor()
        con.execute('SELECT *FROM eventos WHERE dia=%s',(fecha,))
        data = con.fetchall()
        idUsuario = session['id']
        return render_template("index.html", data=data, idUsuario = idUsuario)

@app.route("/filedescripcion", methods=['POST'])

def filedescripcion():
    if request.method == "POST":
        descripcion ="%" + request.form['descripcion'] + "%"
        con = mysql.connection.cursor()
        idUsuario = session['id']
        con.execute('SELECT * FROM eventos WHERE descripcion LIKE  %s',(descripcion,))
        
        data = con.fetchall()
        print("hola")
        print(data)
        return render_template("index.html", data=data, idUsuario = idUsuario)
if __name__ == '__main__':
    app.run(port= 3000, debug=True)







