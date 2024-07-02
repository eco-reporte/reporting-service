from flask import request, jsonify
from reports.application.services.report_service import ReportService

class ReportController:
    def __init__(self, report_service):
        self.report_service = report_service

    def create_report(self):
        report_data = request.get_json()
        new_report = self.report_service.create_report(report_data)
        return jsonify({'message': 'Reporte creado exitosamente', 'reporte': new_report}), 201
