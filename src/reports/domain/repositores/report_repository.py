# report_repository.py
from src.database.database import db
from src.reports.domain.entities.report import Report

class ReportRepository:
    def create(self, report_data):
        report = Report(**report_data)
        db.session.add(report)
        db.session.commit()
        return report

    def get_by_id(self, report_id):
        return db.session.query(Report).get(report_id)

    def get_all(self):
        return db.session.query(Report).all()

    def update(self, report):
        db.session.merge(report)
        db.session.commit()
        return report

    def delete(self, report_id):
        report = self.get_by_id(report_id)
        if report:
            db.session.delete(report)
            db.session.commit()
        return report
    
    