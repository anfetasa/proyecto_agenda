
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'agenda'
mysql = MySQL(app)


app.secret_key = "urioe28934r8ee78rg9iue2h3u4ytg89i3rj958tj4398r"

@app.route("/")
def index():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM eventos")
    data = con.fetchall()
    return render_template("index.html", data=data)


@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        hora = request.form['hora']
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        con = mysql.connection.cursor()
        con.execute("INSERT INTO eventos (titulo,hora,dia,descripcion) VALUES (%s,%s,%s,%s)",
                    (titulo, hora, fecha, descripcion,))
        mysql.connection.commit()
        return redirect(url_for("index"))

@app.route("/borrar/<string:id>")
def borrar(id):
    con = mysql.connection.cursor()
    con.execute("DELETE FROM eventos WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("index"))


@app.route('/cambiar/<id>', methods=['POST', 'GET'])
def cambiar(id):
    con = mysql.connection.cursor()
    con.execute('SELECT * FROM eventos WHERE id = %s', (id,))
    data = con.fetchall()
    con.close()
    return render_template('change.html', data=data)


@app.route("/cambiarc/<id>", methods=['POST'])
def cambiarc(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        hora = request.form['hora']
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        con = mysql.connection.cursor()
        con.execute("""
            UPDATE eventos SET titulo = %s, hora = %s, dia = %s, descripcion = %s WHERE id = %s """, (titulo, hora, fecha, descripcion, id,))
        mysql.connection.commit()
        return redirect(url_for('index'))

if __name__== "__main__":
	app.run(debug=True)