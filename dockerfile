FROM python:3.12

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpq-dev \
    libssl-dev

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt .

# Actualizar pip, setuptools y wheel
RUN pip install --upgrade pip setuptools wheel

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto y ejecutar la aplicación
EXPOSE 5000
CMD ["python", "app.py"]
