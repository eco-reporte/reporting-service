from flask import Blueprint, request, jsonify
from src.reports.application.services.report_service import ReportService

class StatisticsController:
    def __init__(self, report_service: ReportService):
        self.report_service = report_service

    def get_report_count_by_type(self):
        try:
            counts = self.report_service.get_report_count_by_type()
            return jsonify(counts), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_statistics_by_category(self):
        category = request.args.get('category')
        if not category:
            return jsonify({'error': 'Category parameter is required'}), 400
        
        try:
            stats = self.report_service.get_statistics_by_category(category)
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
