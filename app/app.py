from flask import Flask, render_template, request, redirect, url_for, flash
from email.mime.text import MIMEText
from pymongo import MongoClient
from model import Paciente
import smtplib
import random
import bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configuracion de MongoDB
client = MongoClient(host='test_mongodb', port=27017, username='root', password='pass', authSource="admin")
db = client['asp_leg']
mis_pacientes = db['pacientes']
codigos_verificacion = {}
# Para almacenar una contraseña de manera segura
password = "contrasena_secreta".encode('utf-8')
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

@app.route("/", methods=["GET"])
def mostrar_inicio():
    return render_template("index.html")

@app.route("/registro", methods=["GET"])
def mostrar_formulario():
    return render_template("registro.html")

@app.route("/registrar", methods=["POST"])
def registrar_usuario():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    genero = request.form["genero"]
    email = request.form["email"]
    contrasena = request.form["contrasena"]
    confirmar_contrasena = request.form["confirmar_contrasena"]
    codigo_postal = request.form["codigo_postal"]
    localidad = request.form["localidad"]
    provincia = request.form["provincia"]
    historial = request.form["historial_medico"]

    # Realiza validaciones de datos aquí según tus requisitos.
    if contrasena != confirmar_contrasena:
        flash("Las contraseñas no coinciden. Inténtalo de nuevo.", "error")
        return render_template("registro.html",nombre=nombre,apellido=apellido,email=email,fecha_nacimiento=fecha_nacimiento,genero = genero,codigo_postal = codigo_postal,localidad=localidad,provincia=provincia,historial=historial)

    # Genera un código de verificación único.
    codigo_verificacion = str(random.randint(100000, 999999))
    codigos_verificacion[email] = codigo_verificacion
    enviar_correo(email, codigo_verificacion)
    flash("Se ha enviado un codigo de validación al correo electrónico.", "success")
    # Hashea la contraseña antes de almacenarla
    hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
    paciente = Paciente(nombre, apellido, email, hashed_password, fecha_nacimiento,localidad, genero,codigo_postal,provincia,historial)
    try:
        # Guarda el paciente en MongoDB
        db.pacientes.insert_one(paciente.__dict__)
        flash("Paciente registrado con éxito", "success")

    except Exception as e:
        flash(f"Error al registrar al paciente: {str(e)}", "error")
    # return redirect(url_for("insertar"))
    return redirect(url_for("mostrar_formulario"))

def enviar_correo(destinatario, codigo_verificacion):
    remitente = "martinarcosvargas2@gmail.com"  # Cambia esto a tu dirección de correo electrónico de Gmail
    contraseña = "gdvmpiixvmrjofhl"
    mensaje = MIMEText(f"Tu código de verificación es: {codigo_verificacion}", _charset="utf-8")
    # mensaje = f"Tu código de verificación es: {codigo_verificacion}"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, contraseña)
        server.sendmail(remitente, destinatario, mensaje.as_string())
        server.quit()
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {str(e)}")

@app.route("/ver_pacientes")
def ver_pacientes():
    datos = mis_pacientes.find()  # Recupera todos los documentos en la colección
    # return render_template('ver_datos.html')
    return render_template('ver_datos.html', datos=datos)

# def get_db():
#     client = MongoClient(host='test_mongodb', port=27017,  username='root', password='pass', authSource="admin")
#     db = client["animal_db"]
#     return db

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)