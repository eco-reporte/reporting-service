from flask import Blueprint
from src.reports.infraestructure.controllers.statistics_controller import StatisticsController
from src.reports.application.services.report_service import ReportService

bp = Blueprint('statistics_routes', __name__)

def create_statistics_blueprint(report_service: ReportService):
    controller = StatisticsController(report_service)

    @bp.route('/report-count-by-type', methods=['GET'])
    def report_count_by_type():
        return controller.get_report_count_by_type()

    @bp.route('/statistics-by-category', methods=['GET'])
    def statistics_by_category():
        return controller.get_statistics_by_category()

    return bp
