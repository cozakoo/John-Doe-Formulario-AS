from datetime import datetime

class Paciente:
    def __init__(self, nombre, apellido, email, contrasena, fecha_nacimiento,localidad, genero,codigo_postal,provincia, historial):    
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasena = contrasena
        self.fecha_nacimiento = fecha_nacimiento
        self.localidad = localidad
        self.genero = genero
        self.codigo_postal = codigo_postal
        self.provincia = provincia
        self.historial = historial