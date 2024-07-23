# src/reports/domain/entities/estadistica_reporte.py

from mongoengine import Document, StringField, DateTimeField

class EstadisticaReporte(Document):
    causa = StringField(required=True, max_length=100)
    ubicacion = StringField(required=True, max_length=200)
    afectado = StringField(required=True, max_length=200)
    fecha_creacion = DateTimeField(required=True)
    tipo_reporte = StringField(required=True, max_length=100)

    meta = {'collection': 'estadisticas_reportes'}