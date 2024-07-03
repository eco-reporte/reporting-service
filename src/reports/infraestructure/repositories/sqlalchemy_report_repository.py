# src/reports/infraestructure/repositories/sqlalchemy_report_repository.py

from database.database import db
from database.model import Reporte

class SQLAlchemyReportRepository:
    def create(self, report_data):
        new_report = Reporte(
            titulo_reporte=report_data.get('titulo_reporte'),
            tipo_reporte=report_data.get('tipo_reporte'),
            descripcion=report_data.get('descripcion'),
            colonia=report_data.get('colonia'),
            codigo_postal=report_data.get('codigo_postal'),
            imagen_url=report_data.get('imagen_url')
        )
        db.session.add(new_report)
        db.session.commit()
        return new_report
