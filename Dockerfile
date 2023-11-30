# Utilizar una imagen de Python oficial como base
FROM python:3.9-slim-buster

# Instalar dependencias del sistema operativo
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libssl-dev \
    swig \
    build-essential \
    libpq-dev  # Nueva línea para instalar libpq-dev

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos e instalar dependencias
COPY requirements.txt .

# Actualizar pip y setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Instalar oscrypto y endesive
RUN pip install --no-cache-dir --upgrade oscrypto endesive

# Instalar PyKCS11
RUN pip install --no-cache-dir PyKCS11

# Instalar psycopg2-binary en lugar de psycopg2
RUN pip install --no-cache-dir psycopg2-binary

# Instalar otras dependencias desde requirements.txt
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

RUN echo "Instalando dependencias..."
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "Dependencias instaladas correctamente."

# Copiar la aplicación al directorio de trabajo
COPY ./app /app

# Establecer el comando predeterminado
CMD ["python", "app.py"]
