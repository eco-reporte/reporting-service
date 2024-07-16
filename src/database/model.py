from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Reporte(Document):
    titulo_reporte = StringField(required=True, max_length=200)
    nombres = StringField(max_length=100)
    apellidos = StringField(max_length=100)
    telefono = StringField(max_length=20)
    correo = StringField(max_length=100)
    tipo_reporte = StringField(max_length=100)
    descripcion = StringField()
    colonia = StringField(max_length=200)
    codigo_postal = StringField(max_length=20)
    imagen_url = StringField(max_length=200)
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    pdf_url = StringField(max_length=200)

    meta = {'collection': 'reportes'}