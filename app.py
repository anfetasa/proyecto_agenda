
@app.route("/eventos")
def eventos():
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

