from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# *-* coding: utf-8 *-*
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms

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



def firmarcertificado(contraseña, certificado, pdf):
    print("-------Firmador.py----",contraseña, certificado, pdf)
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    with open(pdf, 'rb') as pdf_file:
        date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
        dct = {
            "aligned": 0,
            "sigflags": 3,
            "sigflagsft": 132,
            "sigpage": 0,
            "sigbutton": True,
            "sigfield": "Signature1",
            "auto_sigfield": True,
            "sigandcertify": True,
            "signaturebox": (470, 840, 570, 640),
            "signature": "Aquí va la firma",
            # "signature_img": "signature_test.png",
            "contact": "hola@ejemplo.com",
            "location": "Ubicación",
            "signingdate": date,
            "reason": "Razón",
            "password": contraseña,
        }
        #with open("cert.p12", "rb") as fp:
        p12 = pkcs12.load_key_and_certificates(
            certificado.read(), contraseña.encode("ascii"), backends.default_backend()
        )
        print("********asdasd*******")
        #datau = open(fname, "rb").read()
        datau = pdf_file.read()
        # print("------ARCHIVO datau-----",datau)
        datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
        
    return datau, datas
    """
    fname = "test.pdf"
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)
    """