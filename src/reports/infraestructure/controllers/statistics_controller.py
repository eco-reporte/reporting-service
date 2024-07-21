from flask import Blueprint, request, jsonify, send_file
from io import BytesIO

from src.reports.application.services.StatisticsService import StatisticsService

class StatisticsController:
    def __init__(self, statistics_service: StatisticsService):
        self.statistics_service = statistics_service

    def get_report_count_by_type(self):
        try:
            counts = self.statistics_service.get_report_count_by_type()
            return jsonify(counts), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_statistics_by_category(self):
        category = request.args.get('category')
        if not category:
            return jsonify({'error': 'Category parameter is required'}), 400
        
        try:
            stats = self.statistics_service.get_statistics_by_category(category)
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_top_causes(self):
        top_n = request.args.get('top_n', default=10, type=int)
        try:
            top_causes = self.statistics_service.get_top_causes(top_n)
            return jsonify(top_causes), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_pie_chart(self):
        try:
            chart_bytes = self.statistics_service.generate_pie_chart()
            return send_file(
                BytesIO(chart_bytes),
                mimetype='image/png',
                as_attachment=True,
                download_name='pie_chart.png'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_time_series_chart(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        try:
            chart_bytes = self.statistics_service.generate_time_series_chart(start_date, end_date)
            return send_file(
                BytesIO(chart_bytes),
                mimetype='image/png',
                as_attachment=True,
                download_name='time_series_chart.png'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_bar_chart(self):
        try:
            chart_bytes = self.statistics_service.generate_bar_chart()
            return send_file(
                BytesIO(chart_bytes),
                mimetype='image/png',
                as_attachment=True,
                download_name='bar_chart.png'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500