from database.database import db

class Reporte(db.Model):
    __tablename__ = 'reportes'
    id = db.Column(db.Integer, primary_key=True)
    titulo_reporte = db.Column(db.String(200))
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    tipo_reporte = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    colonia = db.Column(db.String(200))
    codigo_postal = db.Column(db.String(20))
    imagen_url = db.Column(db.String(200))  # Nuevo campo para la URL de la imagen
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    pdf_url = db.Column(db.String(200))  # Nuevo campo para la URL del PDF
    
    def to_dict(self):
        return {
            'id': self.id,
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
            'fecha_creacion': self.fecha_creacion,
            'pdf_url': self.pdf_url
        }
