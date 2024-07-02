from flask import Blueprint, request, jsonify
from reports.application.services.report_service import ReportService
from reports.infraestructure.repositories.sqlalchemy_report_repository import SQLAlchemyReportRepository
from reports.infraestructure.serializers.report_serializer import ReportSerializer

bp = Blueprint('report_routes', __name__)

report_service = ReportService(SQLAlchemyReportRepository())

@bp.route('/reports', methods=['POST'])
def create_report():
    report_data = request.get_json()
    new_report = report_service.create_report(report_data)
    return jsonify(ReportSerializer.serialize(new_report)), 201
