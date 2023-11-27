# syntax=docker/dockerfile:1
FROM python:3.8-slim

# Instalar dependencias del sistema necesarias para compilar algunas bibliotecas Python
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2 \
    libxml2-dev \
    libxslt1.1 \
    libxslt1-dev \
    zlib1g \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar SWIG para solucionar el problema con PyKCS11
RUN apt-get update && apt-get install -y swig

# Actualizar pip y setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos e instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt --use-deprecated=legacy-resolver

# Copiar la aplicación al directorio de trabajo
COPY ./app /app

# Establecer el comando predeterminado
CMD ["python", "app.py"]
