#syntax=docker/dockerfile:1
FROM python:3.8-slim

WORKDIR /app

COPY requerements.txt .

RUN pip install --no-cache-dir -r requerements.txt

COPY app/ app/

CMD ["python", "app/app.py"]