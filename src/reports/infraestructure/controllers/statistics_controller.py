from flask import jsonify, request, send_file
from src.reports.application.services.report_service import ReportService
from datetime import datetime

class StatisticsController:
    def __init__(self, report_service: ReportService):
        self.report_service = report_service

    def get_time_series_chart(self):
        try:
            chart = self.report_service.generate_time_series_chart()
            return send_file(chart, mimetype='image/png')
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_pie_chart(self):
        try:
            chart = self.report_service.generate_pie_chart()
            return send_file(chart, mimetype='image/png')
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_statistics_by_category(self, category):
        try:
            statistics = self.report_service.get_statistics_by_category(category)
            return jsonify([stat.to_dict() for stat in statistics])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_report_count_by_type(self):
        try:
            count_by_type = self.report_service.get_report_count_by_type()
            return jsonify(list(count_by_type))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_time_series_chart_by_date_range(self):
        try:
            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
            chart = self.report_service.generate_time_series_chart(start_date, end_date)
            return send_file(chart, mimetype='image/png')
        except Exception as e:
            return jsonify({'error': str(e)}), 500