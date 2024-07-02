class ReportSerializer:
    @staticmethod
    def serialize(report):
        return {
            'id': report.id,
            'titulo_reporte': report.titulo_reporte,
            'tipo_reporte': report.tipo_reporte,
            'descripcion': report.descripcion,
            'colonia': report.colonia,
            'codigo_postal': report.codigo_postal,
            'fecha_creacion': report.fecha_creacion.isoformat()
        }

    @staticmethod
    def deserialize(data):
        return Report(
            titulo_reporte=data.get('titulo_reporte'),
            tipo_reporte=data.get('tipo_reporte'),
            descripcion=data.get('descripcion'),
            colonia=data.get('colonia'),
            codigo_postal=data.get('codigo_postal')
        )
