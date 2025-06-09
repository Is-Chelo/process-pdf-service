# Imagen base oficial con Python + todas las dependencias de WeasyPrint
FROM python:3.10-slim

# Evita problemas con stdin
ENV PYTHONUNBUFFERED=1

# Instala dependencias del sistema necesarias para WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libglib2.0-0 \
    curl \
    && apt-get clean

# Establece directorio de trabajo
WORKDIR /app

# Copia archivos del proyecto
COPY . /app

# Instala dependencias de Python
RUN pip install --no-cache-dir weasyprint

# Comando por defecto (puedes reemplazarlo si tienes otro script)
CMD ["python", "lambda_function.py"]
