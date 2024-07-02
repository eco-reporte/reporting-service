from reports.domain.repositores.report_repository import ReportRepository

class ReportService:
    def __init__(self, report_repository):
        self.report_repository = report_repository

    def create_report(self, report_data):
        return self.report_repository.create(report_data)