# from flask import Blueprint, request, jsonify, send_file
# from reports.application.services.report_service import ReportService
# from reports.infraestructure.repositories.sqlalchemy_report_repository import SQLAlchemyReportRepository
# from reports.application.services.pdf_services import create_pdf

# import io

# bp = Blueprint('report_routes', __name__)

# report_service = ReportService(SQLAlchemyReportRepository())

# @bp.route('/reports', methods=['POST'])
# def create_report():
#     # Obtener datos del formulario
#     report_data = request.form.to_dict()
#     image_file = request.files['image']

#     # Crear reporte y subir imagen
#     new_report = report_service.create_report(report_data, image_file)
    
#     # Crear PDF
#     pdf = create_pdf(new_report)
    
#     # Enviar PDF como respuesta
#     return send_file(
#         io.BytesIO(pdf),
#         mimetype='application/pdf',
#         as_attachment=True,
#         download_name='report.pdf'
#     )

# src/reports/infraestructure/routes/report_routes.py

from flask import Blueprint, request, jsonify, send_file
from reports.application.services.report_service import ReportService
from reports.infraestructure.repositories.sqlalchemy_report_repository import SQLAlchemyReportRepository
from reports.application.services.pdf_services import create_pdf

import io

bp = Blueprint('report_routes', __name__)

report_service = ReportService(SQLAlchemyReportRepository())

@bp.route('/reports', methods=['POST'])
def create_report():
    # Obtener datos del formulario y archivo de imagen
    report_data = request.form.to_dict()
    image_file = request.files['image']

    # Crear reporte y subir imagen
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
