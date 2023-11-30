# John Doe S.A
Trabajo Práctivo de la materia "Aspectos Legales de la Informatica"
## Tabla de Contenidos

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Licencia](#licencia)

## Descripción

Este proyecto es una aplicación web desarrollada en Python utilizando el framework Flask y MongoDB como base de datos. Proporciona una plataforma que busca explorar la Ley de Protección de Datos Personales y la tecnología de Firma Digital en el contexto de la empresa John Doe S.A., que desarrolla y administra un **sistema hospitalario**.

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

- Python 3.10.7
- MongoDB 7.0
- [Docker](https://www.docker.com/get-started)

## Instalación

Sigue estos pasos para instalar y configurar el proyecto:

1. Clona este repositorio en tu máquina local:

    ```bash
    git clone https://github.com/cozakoo/John-Doe-Formulario-AS.git
2. Ve al directorio del proyecto:
    ```bash
    cd John-Doe-Formulario-AS.git
3. Construye la imagen
    ```bash
    docker build -t sistema-hospitalario-flask .
4. Ejecuta la aplicación en un contenedor:
    ```bash
    docker-compose up
5. Accede a la aplicación en tu navegador web:
    http://localhost:5000    


## Uso

Los pacientes pueden acceder a la aplicación a través de un navegador web visitando la dirección http://localhost:5000 si están ejecutando la aplicación localmente.

##### Registro de Pacientes:

Los pacientes pueden completar su registro proporcionando sus datos personales, dirección de correo electrónico y contraseña en el formulario proporcionado por la aplicación.
Después de enviar el formulario, la aplicación valida que las contraseñas coincidan y, si es así, se procede a la validación del correo electronico.

##### Validación de Correo Electrónico:

Luego de completar el formulario, los pacientes reciben un correo electrónico de validación en la dirección proporcionada.
El correo electrónico contiene un codigo numerico que deben ingresar a la pagina para confirmar su identidad. Si el proceso es exitoso, entonces se registra al paciente en la base de datos.

##### Almacenamiento de Datos en la Base de Datos:

Una vez que los pacientes validen su identidad, el usuario quedara como validada en la base de datos.
Los datos personales de los pacientes se almacenan de manera segura en la base de datos MongoDB.

## Ejemplos

A continuación se proporcionaran algunos ejemplos de uso para que los pacientes puedan interactuar con la aplicación hospitalaria, ingresar sus datos, completar el proceso de validación por correo electrónico y verificar que sus datos se almacenan correctamente en la base de datos.

**Ejemplo 1: Registro de un Nuevo Paciente**

1. Abre un navegador web y ve a `http://localhost:5000`.

2. En la página de inicio, encontrarás la pagina princial. A continuación seleccionar "Alta de paciente". Completa los campos requeridos con los datos personales, dirección de correo electrónico y contraseña. A continuación, un ejemplo de cómo se vería el formulario:

   - Nombre: Juan
   - Apellido: Pérez
   - Correo Electrónico: juan@example.com
   - Contraseña: q4dgv*ZF
   - Confirmar Contraseña: q4dgv*ZF
   - [El resto de los campos]
3. Haz clic en el botón "Registrar Paciente".
4. Deberías ver un mensaje de éxito que indica que se ha enviado un correo de validación a tu dirección de correo electrónico.

**Ejemplo 2: Validación por Correo Electrónico**

1. Ve a la bandeja de entrada de tu correo electrónico.

2. Deberías recibir un correo electrónico de validación con un codigo numerico único. El correo electrónico puede tener un asunto como "Valida tu cuenta en el Sistema Hospitalario".

3. Haz clic en el enlace de validación dentro del correo electrónico.

4. Deberías ser redirigido a la aplicación hospitalaria y ver un mensaje de éxito que confirma que tu cuenta ha sido validada correctamente.

5. Si esta todo correto se te enviara un correo informando el nombre y contraseña para poder ingresar al sistema hospitalario

## Licencia

Este proyecto está bajo [Licencia](https://github.com/cozakoo/John-Doe-Formulario-AS/blob/main/LICENSE). Consulte el archivo LICENSE para obtener más detalles.