from flask import Blueprint, request, jsonify, send_file
from reports.application.services.report_service import ReportService
from reports.infraestructure.repositories.sqlalchemy_report_repository import SQLAlchemyReportRepository
from reports.application.services.pdf_services import create_pdf

import io

bp = Blueprint('report_routes', __name__)
report_service = ReportService(SQLAlchemyReportRepository())

@bp.route('/reports', methods=['POST'])
def create_report():
    report_data = request.form.to_dict()
    image_file = request.files['image']

    new_report = report_service.create_report(report_data, image_file)
    
    # Crear PDF
    pdf = create_pdf(new_report)
    
    # Enviar PDF como respuesta
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='report.pdf'
    )


# from flask import request, jsonify
# from reports.application.services.report_service import ReportService

# class ReportController:
#     def __init__(self, report_service):
#         self.report_service = report_service

#     def create_report(self):
#         report_data = request.get_json()
#         new_report = self.report_service.create_report(report_data)
#         return jsonify({'message': 'Reporte creado exitosamente', 'reporte': new_report}), 201
