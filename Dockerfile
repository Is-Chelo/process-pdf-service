FROM python:3.11-slim

# Evita errores con variables regionales
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema para WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    zlib1g-dev \
    fonts-liberation \
    fonts-dejavu \
    fontconfig \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY . .

# Instalar weasyprint
RUN pip install --no-cache-dir weasyprint

# Ejecutar el script
CMD ["python", "lambda_function.py"]
