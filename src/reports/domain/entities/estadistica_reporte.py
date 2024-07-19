from mongoengine import Document, StringField, DateTimeField

class EstadisticaReporte(Document):
    categoria = StringField(required=True, max_length=100)
    que_paso = StringField(required=True, max_length=200)
    donde_paso = StringField(required=True, max_length=200)
    a_quien_paso = StringField(required=True, max_length=200)
    fecha = DateTimeField(required=True)

    meta = {'collection': 'estadisticas_reportes'}
