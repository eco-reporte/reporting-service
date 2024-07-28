FROM python:3.12

WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos
COPY requirements.txt ./

# Actualiza pip, setuptools y wheel
RUN pip install --upgrade pip setuptools wheel

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expon la aplicación en el puerto 3000 (ajusta si es necesario)
EXPOSE 3000

# Define el comando de entrada
CMD ["python", "app.py"]
