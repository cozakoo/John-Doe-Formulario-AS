from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session, g, send_file, make_response

from io import BytesIO
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader

from pymongo import MongoClient
from model import Paciente
from werkzeug.security import generate_password_hash, check_password_hash

import io , random, bcrypt, os

from funciones import *

app = Flask(__name__)

app.secret_key = "clave_secreta"
# Conexion con Docker
# client = MongoClient(host='test_mongodb', port=27017, username='root', password='pass', authSource="admin")

# Conexion local
client = MongoClient(host='localhost', port=27017)

db = client['asp_leg']
mis_usuarios = db["usuarios"]
mis_pacientes = db['pacientes']
codigos_verificacion = {}
# Para almacenar una contraseña de manera segura
password = "contrasena_secreta".encode('utf-8')
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
correo_enviado = False
codigo_verificacion_ingresado = ""
codigo_verificacion = ""

# Middleware para cargar el paciente en el contexto global
@app.before_request
def before_request():
    g.paciente = None  # Inicializa g.paciente


@app.route('/')
def index():
    # Redirige a la página de inicio de sesión si el usuario no está autenticado
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Busca al usuario en MongoDB
        user = mis_usuarios.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            # Si las credenciales son válidas, establece la sesión y redirige al dashboard
            session['username'] = username
            session['user_type'] = user.get('user_type', 'default_user_type')  # Establece el tipo de usuario en la sesión
            return redirect(url_for('dashboard'))
        else:
            # Si el usuario no existe o las credenciales no coinciden, muestra un mensaje de error
            flash('Usuario o contraseña incorrectos', 'error')

    return render_template('auth/login.html')

@app.route('/dashboard')
def dashboard():
    # Verifica si el usuario está autenticado antes de mostrar el dashboard
    if 'username' not in session:
        flash('Debes iniciar sesión primero', 'error')
        return redirect(url_for('login'))

    # Obtiene el tipo de usuario desde la base de datos
    username = session['username']
    user_data = mis_usuarios.find_one({'username': username})

    if user_data is None:
        flash('Error al obtener información del usuario', 'error')
        return redirect(url_for('login'))

    user_type = user_data.get('user_type', 'default_user_type')

    # Resto de la lógica para mostrar el dashboard según el tipo de usuario
    return render_template('dashboard.html', user_type=user_type)


@app.route('/logout')
def logout():
    # Elimina la información de la sesión para cerrar sesión
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        # Verifica si el usuario ya existe
        if mis_usuarios.find_one({'username': username}):
            flash('Usuario ya existente', 'error')
            return render_template('create_user.html')

        hashed_password = generate_password_hash(password, method='sha256')

        # Guarda el nuevo usuario en MongoDB con el tipo de usuario
        mis_usuarios.insert_one({
            'username': username,
            'password': hashed_password,
            'user_type': user_type
        })
        flash('Usuario creado con éxito', 'success')
        return redirect(url_for('login'))

    return render_template('create_user.html')


@app.route('/registrar_paciente')
def registrar_paciente():
        # Aquí puedes agregar la lógica necesaria para el registro de pacientes
    return render_template('registrar_paciente.html')  # Reemplaza con tu propia plantilla

# validacion de captcha y re captcha y validacion del correo
@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    global correo_enviado
    global codigo_verificacion_ingresado
    global codigo_verificacion
    dni = request.form["dni"]
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

    # si las contraseñas no coinciden
    if contrasena != confirmar_contrasena:
        flash("Las contraseñas no coinciden. Inténtalo de nuevo.", "error")
        return render_template("registrar_paciente.html", nombre=nombre, apellido=apellido, fecha_nacimiento=fecha_nacimiento, genero = genero, email=email, codigo_postal = codigo_postal, localidad=localidad, provincia=provincia, historial=historial)

    datos_formulario = {
        'dni' : dni,
        'nombre': nombre,
        'apellido': apellido,
        'fecha_nacimiento': fecha_nacimiento,
        'genero': genero,
        'email': email,
        'codigo_postal': codigo_postal,
        'localidad': localidad,
        'provincia': provincia,
        'historial_medico': historial,
        'contrasena': contrasena,
        'confirmar_contrasena': confirmar_contrasena
    }

    # Si el correo no ha sido enviado para verificar lo envia.
    if not correo_enviado:
        # Genera un código de verificación único.
        codigo_verificacion = str(random.randint(100000, 999999))
        codigos_verificacion[email] = codigo_verificacion
        enviar_correo_validacion(email, codigo_verificacion)
        correo_enviado = True
        flash("Se ha enviado un codigo de validación al correo electrónico.", "success")
        return render_template("registrar_paciente.html", **datos_formulario)

    codigo_verificacion_ingresado = request.form["codigo_verificacion"]
    if codigo_verificacion_ingresado != codigo_verificacion:
        flash("El código de verificación no es válido. Inténtalo de nuevo.", "error")
        return render_template("registrar_paciente.html", **datos_formulario)

    try:
        # guarda la contraseña de manera segura
        hashed_password = generate_password_hash(contrasena, method='sha256')

        paciente = Paciente(dni, nombre, apellido, email, hashed_password, fecha_nacimiento,localidad, genero,codigo_postal,provincia,historial)
        # Guarda el paciente en MongoDB
        db.pacientes.insert_one(paciente.__dict__)

        nombre_usuario = nombre.lower() + '_' + apellido.lower()
        mis_usuarios.insert_one({
            'username': nombre_usuario,
            'password': hashed_password,
            'user_type': 'patient',
            'dni' : dni
        })
        
        enviar_correo_registro(email, nombre_usuario, contrasena)
        flash("Paciente registrado con éxito, se le ha enviado un correo al paciente", "success")

    except Exception as e:
        flash(f"Error al registrar al paciente: {str(e)}", "error")
    # return redirect(url_for("insertar"))
    return redirect(url_for('dashboard'))



@app.route("/listar_pacientes")
def listar_pacientes():
    # Verifica si el usuario está autenticado
    if 'username' not in session:
        return redirect(url_for('login'))

    user_type = session.get('user_type', 'default_user_type')
    # Si el usuario es un paciente, solo muestra sus propios datos
    username = session.get('username')
    if user_type == 'patient':
        usuario = mis_usuarios.find_one({'username': username})
        if usuario:
            dni_ = usuario.get('dni')
            paciente = mis_pacientes.find_one({'dni': dni_})
            return render_template('ver_paciente.html', paciente=paciente)

    #Si el usuario es admin o secretario, muestra la lista completa de pacientes
    if user_type in ['admin', 'secretary']:
        pacientes = mis_pacientes.find({})
        return render_template('listar_pacientes.html', pacientes=pacientes)

    return render_template('dashboard')


@app.route('/recetaMedica/<paciente_id>')
def recetaMedica(paciente_id):
    g.paciente = mis_pacientes.find_one({'dni': paciente_id})
    return render_template("recetaMedica.html", paciente=g.paciente)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Obtener datos del paciente desde el formulario
    paciente_data = {
        'dni': request.form['dni'],
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'fecha_nacimiento': request.form['fecha_nacimiento'],
        'historial': request.form['historial'],
    }

    # Crear el PDF en memoria
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    
    # Agregar la información del paciente al PDF
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 750, f'Dni: {paciente_data["dni"]}')
    pdf.drawString(100, 720, f"Nombre y Apellido: {paciente_data['nombre']} {paciente_data['apellido']}")
    pdf.drawString(100, 690, f'nacimiento: {paciente_data["fecha_nacimiento"]}')
    pdf.drawString(100, 660, f'email: {paciente_data["email"]}')
    pdf.drawString(100, 630, f'Historial: {paciente_data["historial"]}')
    
    # Agregar la receta médica al PDF (cambiar según la ubicación deseada)
    medicamento = request.form['medicamento']
    pdf.drawString(100, 600, f'Receta médica')
    pdf.drawString(130, 570, medicamento)

    # Guardar el estado del PDF y cerrar el objeto PDF
    pdf.showPage()
    pdf.save()

    # Configurar la respuesta para devolver el PDF en lugar de guardarlo en un archivo
    buffer.seek(0)
    response = make_response(buffer.read())
    buffer.close()

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=receta_medica.pdf'

    # Firmar el PDF
    return response

@app.route('/firmar', methods=['GET'])
def firmar():
    return render_template("formulario.html")

@app.route('/procesar', methods=['POST'])
def procesar():
    pdf = request.files.get("pdf")
    firma = request.files.get("firma")
    contraseña = request.form.get("palabra_secreta")
    archivo_pdf_para_enviar_al_cliente = io.BytesIO()

    try:
        datau, datas = firmar(contraseña, firma, pdf)
        archivo_pdf_para_enviar_al_cliente.write(datau)
        archivo_pdf_para_enviar_al_cliente.write(datas)
        archivo_pdf_para_enviar_al_cliente.seek(0)

        return send_file(archivo_pdf_para_enviar_al_cliente, mimetype="application/pdf",
                         download_name="firmado" + ".pdf",
                         as_attachment=True)
    except ValueError as e:
        return "Error firmando: " + str(e) + ". Se recomienda revisar la contraseña y el certificado"





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)