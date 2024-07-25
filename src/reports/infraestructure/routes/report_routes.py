from flask import Blueprint
from src.reports.infraestructure.controllers.report_controller import ReportController
from src.reports.application.services.report_service import ReportService

def create_report_blueprint(report_service: ReportService, report_controller: ReportController):
    blueprint = Blueprint('reports', __name__)

    @blueprint.route('/', methods=['POST'])
    def create_report():
        return report_controller.create_report()

    @blueprint.route('/', methods=['GET'])
    def get_all_reports():
        return report_controller.get_all_reports()

    @blueprint.route('/<string:report_id>', methods=['GET'])
    def get_report(report_id):
        return report_controller.get_report(report_id)

    @blueprint.route('/<string:report_id>', methods=['PUT'])
    def update_report(report_id):
        return report_controller.update_report(report_id)

    @blueprint.route('/<string:report_id>', methods=['PATCH'])
    def patch_report(report_id):
        return report_controller.patch_report(report_id)

    @blueprint.route('/<string:report_id>', methods=['DELETE'])
    def delete_report(report_id):
        return report_controller.delete_report(report_id)

    @blueprint.route('/', methods=['DELETE'])
    def delete_all_reports():
        return report_controller.delete_all_reports()
    
    @blueprint.route('/pdf-list', methods=['GET'])
    def get_pdf_list():
        return report_controller.get_pdf_list()
    
    @blueprint.route('/<string:report_id>/status', methods=['PATCH'])
    def update_report_status(report_id):
        return report_controller.patch_report(report_id)

    return blueprint