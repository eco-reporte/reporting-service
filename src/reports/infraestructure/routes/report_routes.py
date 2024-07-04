# reports/infraestructure/routes/report_routes.py

from flask import Blueprint, request, jsonify, send_file
from reports.application.services.report_service import ReportService
from reports.infraestructure.repositories.sqlalchemy_report_repository import SQLAlchemyReportRepository
from reports.application.services.pdf_services import create_pdf
import io

bp = Blueprint('report_routes', __name__)

report_service = ReportService(SQLAlchemyReportRepository())

@bp.route('/reports', methods=['POST'])
def create_report():
    # Obtener datos del formulario
    report_data = request.form.to_dict()
    image_file = request.files['image']

    # Crear reporte y subir imagen
    new_report = report_service.create_report(report_data, image_file)
    
    # Crear PDF
    pdf, filename = create_pdf(new_report)
    
    # Enviar PDF como respuesta
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@bp.route('/reports', methods=['GET'])
def get_all_reports():
    reports = report_service.get_all_reports()
    return jsonify([report.to_dict() for report in reports])

@bp.route('/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    report = report_service.get_report_by_id(report_id)
    return jsonify(report.to_dict())

@bp.route('/reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    report_data = request.json
    report = report_service.get_report_by_id(report_id)
    for key, value in report_data.items():
        setattr(report, key, value)
    report_service.update_report(report)
    return jsonify(report.to_dict())

@bp.route('/reports/<int:report_id>', methods=['PATCH'])
def patch_report(report_id):
    report_data = request.json
    report = report_service.get_report_by_id(report_id)
    for key, value in report_data.items():
        setattr(report, key, value)
    report_service.update_report(report)
    return jsonify(report.to_dict())

@bp.route('/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    report_service.delete_report(report_id)
    return jsonify({'message': 'Report deleted successfully'})
