# Usa una imagen base de Python 3.12
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 3003

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]