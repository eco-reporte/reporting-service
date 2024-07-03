from database.database import db

class Reporte(db.Model):
    __tablename__ = 'reportes'
    id = db.Column(db.Integer, primary_key=True)
    titulo_reporte = db.Column(db.String(200))
    tipo_reporte = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    colonia = db.Column(db.String(200))
    codigo_postal = db.Column(db.String(20))
    imagen_url = db.Column(db.String(300))  # Campo para almacenar la URL de la imagen
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
