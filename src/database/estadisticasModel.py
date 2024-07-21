from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class EstadisticaReporte(Document):
    causa = StringField()
    ubicacion = StringField()
    afectado = StringField()
    fecha_creacion = DateTimeField()
    tipo_reporte = StringField()
    
    meta = {'collection': 'estadisticas_reportes'}
