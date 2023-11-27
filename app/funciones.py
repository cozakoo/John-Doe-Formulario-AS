from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def enviar_correo_registro(destinatario,username, password ):
    remitente = "martinarcosvargas2@gmail.com"  # Cambia esto a tu dirección de correo electrónico de Gmail
    contraseña = "gdvmpiixvmrjofhl"
    # URL de inicio de sesión
    url_login = "http://127.0.0.1:5000/login"
    #Partes del correo
    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = "¡Usuario creado con éxito en el sistema hospitalario!"
    saludo = f"Hola!"

    cuerpo_mensaje = (
        f"{saludo}\n\n"
        "¡Bienvenido a nuestro sistema hospitalario!\n\n"
        f"Tu usuario para ingresar es: {username}\n"
        f"Tu contraseña es: {password}\n\n"
        f"Puedes iniciar sesión haciendo clic en el siguiente enlace:\n"
        f"{url_login}\n\n"
        "No responder a este correo.\n"
        "Gracias y que tengas un buen día."
    )
    mensaje.attach(MIMEText(cuerpo_mensaje, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, contraseña)
        server.sendmail(remitente, destinatario, mensaje.as_string())
        server.quit()
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {str(e)}")

def enviar_correo_validacion(destinatario, codigo_verificacion):
    remitente = "martinarcosvargas2@gmail.com"  # Cambia esto a tu dirección de correo electrónico de Gmail
    contraseña = "gdvmpiixvmrjofhl"

    #Partes del correo
    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = "Valida tu cuenta en el Sistema Hospitalario"

    cuerpo_mensaje = f"Tu código de verificación es: {codigo_verificacion}"
    mensaje.attach(MIMEText(cuerpo_mensaje, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, contraseña)
        server.sendmail(remitente, destinatario, mensaje.as_string())
        server.quit()
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {str(e)}")