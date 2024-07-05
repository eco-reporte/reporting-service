# reports/infraestructure/routes/report_routes.py

from flask import Blueprint
from reports.infraestructure.controllers.report_controller import ReportController
from reports.application.services.report_service import ReportService
from reports.infraestructure.repositories.sqlalchemy_report_repository import SQLAlchemyReportRepository

bp = Blueprint('report_routes', __name__)
report_service = ReportService(SQLAlchemyReportRepository())
report_controller = ReportController(report_service)

@bp.route('/reports', methods=['POST'])
def create_report():
    return report_controller.create_report()

@bp.route('/reports', methods=['GET'])
def get_all_reports():
    return report_controller.get_all_reports()

@bp.route('/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    return report_controller.get_report(report_id)

@bp.route('/reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    return report_controller.update_report(report_id)

@bp.route('/reports/<int:report_id>', methods=['PATCH'])
def patch_report(report_id):
    return report_controller.patch_report(report_id)

@bp.route('/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    return report_controller.delete_report(report_id)

@bp.route('/reports/<int:report_id>/pdf', methods=['GET'])
def get_report_pdf(report_id):
    return report_controller.get_report_pdf(report_id)

@bp.route('/reports/pdfs', methods=['GET'])
def get_all_pdfs():
    return report_controller.get_all_pdfs()

@bp.route('/reports/pdfs/download', methods=['GET'])
def download_all_pdfs():
    return report_controller.download_all_pdfs()

@bp.route('/reports', methods=['DELETE'])
def delete_all_reports():
    return report_controller.delete_all_reports()