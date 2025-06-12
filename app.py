from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de conexión a MySQL
db_config = {
    'host': '127.0.0.1',
    'user': 'root',        # Cambia esto por tu usuario de MySQL (ej: 'root')
    'password': 'entrecodigosycafe', # Cambia esto por tu contraseña de MySQL
    'database': 'mi_formulario', # Nombre de la base de datos
    'port': 33060                 # Si usas otro puerto, cámbialo aquí
}

# Ruta para mostrar el formulario
@app.route('/')
def formulario():
    return render_template('form.html')

# Ruta para procesar el formulario
@app.route('/enviar', methods=['POST'])
def enviar():
    # Obtener los datos del formulario
    nombre = request.form['nombre']
    correo = request.form['correo']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    fecha_nacimiento = request.form['fecha_nacimiento']
    genero = request.form['genero']

    # Conectar a la base de datos y guardar los datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insertar los datos en la base de datos
    query = """
    INSERT INTO usuarios (nombre, correo, telefono, direccion, fecha_nacimiento, genero)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, correo, telefono, direccion, fecha_nacimiento, genero))
    conn.commit()

    cursor.close()
    conn.close()

    # Redirigir a la página de registros
    return redirect(url_for('ver_registros'))

# Ruta para ver los registros
@app.route('/registros')
def ver_registros():
    # Conectar a la base de datos y obtener los registros
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Obtener todos los registros de la base de datos
    cursor.execute("SELECT * FROM usuarios")
    registros = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('records.html', registros=registros)

if __name__ == '__main__':
    app.run(debug=True)
