from flask import Blueprint, jsonify, current_app

bp = Blueprint('statistics', __name__)

@bp.route('/time-series', methods=['GET'])
def get_time_series():
    report_service = current_app.report_service
    chart_data = report_service.generate_time_series_chart()
    return jsonify(chart_data)

@bp.route('/pie-chart', methods=['GET'])
def get_pie_chart():
    report_service = current_app.report_service
    chart_data = report_service.generate_pie_chart()
    return jsonify(chart_data)

@bp.route('/category/<string:category>', methods=['GET'])
def get_statistics_by_category(category):
    report_service = current_app.report_service
    statistics = report_service.get_statistics_by_category(category)
    return jsonify(statistics)

@bp.route('/report-count', methods=['GET'])
def get_report_count():
    report_service = current_app.report_service
    count = report_service.get_report_count_by_type()
    return jsonify(count)