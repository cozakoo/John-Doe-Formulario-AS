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
    docker build -t aspectos-legales-flask -f Dockerfile .
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

Luego de registrarse, los pacientes reciben un correo electrónico de validación en la dirección proporcionada.
El correo electrónico contiene un enlace de validación único que deben ingresar a la pagina para confirmar su identidad. Si el proceso es exitoso, entonces se registra al paciente en la base de datos.

##### Almacenamiento de Datos en la Base de Datos:

Una vez que los pacientes validen su identidad, la aplicación marca su cuenta como validada en la base de datos.
Los datos personales de los pacientes se almacenan de manera segura en la base de datos MongoDB.

## Licencia

Este proyecto está bajo [Licencia](https://github.com/cozakoo/John-Doe-Formulario-AS/blob/main/LICENSE). Consulte el archivo LICENSE para obtener más detalles.