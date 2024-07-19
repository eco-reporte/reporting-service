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

    def to_dict(self):
        return {
            'id': str(self.id),
            'titulo_reporte': self.titulo_reporte,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'telefono': self.telefono,
            'correo': self.correo,
            'tipo_reporte': self.tipo_reporte,
            'descripcion': self.descripcion,
            'colonia': self.colonia,
            'codigo_postal': self.codigo_postal,
            'imagen_url': self.imagen_url,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'pdf_url': self.pdf_url
        }
    
class EstadisticasReporte(Document):
    causa = StringField(max_length=200)
    ubicacion = StringField(max_length=200)
    afectado = StringField(max_length=200)
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    tipo_reporte = StringField(max_length=100)

    meta = {'collection': 'estadisticas_reportes'}