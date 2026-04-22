from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("citas.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            mascota   TEXT NOT NULL,
            propietario TEXT NOT NULL,
            especie   TEXT,
            fecha     TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db()
    pacientes = conn.execute("SELECT * FROM pacientes").fetchall()
    conn.close()
    return render_template("index.html", pacientes=pacientes)

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        mascota     = request.form['mascota']
        propietario = request.form['propietario']
        especie     = request.form['especie']
        fecha       = request.form['fecha']

        conn = get_db()
        conn.execute(
            "INSERT INTO pacientes (mascota, propietario, especie, fecha) VALUES (?, ?, ?, ?)",
            (mascota, propietario, especie, fecha)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template("agendar.html")

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    conn = get_db()

    if request.method == 'POST':
        mascota     = request.form['mascota']
        propietario = request.form['propietario']
        especie     = request.form['especie']
        fecha       = request.form['fecha']

        conn.execute(
            "UPDATE pacientes SET mascota=?, propietario=?, especie=?, fecha=? WHERE id=?",
            (mascota, propietario, especie, fecha, id)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    paciente = conn.execute("SELECT * FROM pacientes WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("modificar.html", paciente=paciente)

@app.route('/cancelar/<int:id>')
def cancelar(id):
    conn = get_db()
    conn.execute("DELETE FROM pacientes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)