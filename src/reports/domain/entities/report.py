class Report:
    def __init__(self, titulo_reporte, tipo_reporte, descripcion, colonia, codigo_postal, nombres, apellidos, telefono, correo):
        self.titulo_reporte = titulo_reporte
        self.tipo_reporte = tipo_reporte
        self.descripcion = descripcion
        self.colonia = colonia
        self.codigo_postal = codigo_postal
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.correo = correo

    def to_dict(self):
        return {
            'titulo_reporte': self.titulo_reporte,
            'tipo_reporte': self.tipo_reporte,
            'descripcion': self.descripcion,
            'colonia': self.colonia,
            'codigo_postal': self.codigo_postal,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'telefono': self.telefono,
            'correo': self.correo
        }

    def __repr__(self):
        return (f"Report(titulo_reporte={self.titulo_reporte}, tipo_reporte={self.tipo_reporte}, "
                f"descripcion={self.descripcion}, colonia={self.colonia}, codigo_postal={self.codigo_postal}, "
                f"nombres={self.nombres}, apellidos={self.apellidos}, telefono={self.telefono}, correo={self.correo})")
