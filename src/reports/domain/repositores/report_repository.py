from database.database import db
from reports.domain.entities.report import Report

class ReportRepository:
    def create(self, report_data):
        report = Report(**report_data)
        db.session.add(report)
        db.session.commit()
        return report