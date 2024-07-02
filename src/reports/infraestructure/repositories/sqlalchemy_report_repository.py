from database.database import db
from database.model import Reporte


class SQLAlchemyReportRepository:
    def create(self, report_data):
        report = Reporte(**report_data)
        db.session.add(report)
        db.session.commit()
        return report