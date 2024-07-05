# src/reports/infraestructure/repositories/sqlalchemy_report_repository.py

from database.database import db
from database.model import Reporte
from database.model import Reporte


class SQLAlchemyReportRepository:
    def create(self, report_data):
        new_report = Reporte(**report_data)
        db.session.add(new_report)
        db.session.commit()
        return new_report

    def update(self, report):
        db.session.merge(report)
        db.session.commit()
        return report

    def delete(self, report_id):
        report = self.get_by_id(report_id)
        db.session.delete(report)
        db.session.commit()
        return report

    def get_by_id(self, report_id):
        return Reporte.query.get(report_id)

    def get_all(self):
        return Reporte.query.all()
    
    def get_all_pdf_urls(self):
        reports = Reporte.query.all()
        return [report.pdf_url for report in reports]
    
    def delete_all(self):
        deleted_count = db.session.query(Reporte).delete()
        db.session.commit()
        return deleted_count
