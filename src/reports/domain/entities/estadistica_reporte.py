from mongoengine import Document, StringField, DateTimeField

class EstadisticaReporte(Document):
    causa = StringField(required=True, max_length=100)
    ubicacion = StringField(required=True, max_length=200)
    afectado = StringField(required=True, max_length=200)
    fecha_creacion = StringField(required=True, max_length=200)
    tipo_reporte = DateTimeField(required=True)

    meta = {'collection': 'estadisticas_reportes'}
