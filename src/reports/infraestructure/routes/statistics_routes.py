from flask import Blueprint
from src.reports.application.services import StatisticsService
from src.reports.infraestructure.controllers.statistics_controller import StatisticsController

bp = Blueprint('statistics_routes', __name__)

def create_statistics_blueprint(statistics_service: StatisticsService):
    controller = StatisticsController(statistics_service)

    @bp.route('/report-count-by-type', methods=['GET'])
    def report_count_by_type():
        return controller.get_report_count_by_type()

    @bp.route('/statistics-by-category', methods=['GET'])
    def statistics_by_category():
        return controller.get_statistics_by_category()

    @bp.route('/top-causes', methods=['GET'])
    def top_causes():
        return controller.get_top_causes()

    @bp.route('/pie-chart', methods=['GET'])
    def pie_chart():
        return controller.get_pie_chart()

    @bp.route('/time-series-chart', methods=['GET'])
    def time_series_chart():
        return controller.get_time_series_chart()

    @bp.route('/bar-chart', methods=['GET'])
    def bar_chart():
        return controller.get_bar_chart()
    
    @bp.route('/time-series-analysis', methods=['GET'])
    def time_series_analysis():
        return controller.get_time_series_analysis()
    
    @bp.route('/regresion-lineal-multiple', methods=['POST'])
    def regresion_lineal_multiple():
        return controller.regresion_lineal_multiple()

    @bp.route('/descomposicion-clasica', methods=['POST'])
    def descomposicion_clasica():
        return controller.descomposicion_clasica()

    @bp.route('/descomposicion-stl', methods=['POST'])
    def descomposicion_stl():
        return controller.descomposicion_stl()

    @bp.route('/suavizado-exponencial', methods=['POST'])
    def suavizado_exponencial():
        return controller.suavizado_exponencial()

    @bp.route('/random-forest', methods=['POST'])
    def random_forest():
        return controller.random_forest()

    @bp.route('/xgboost', methods=['POST'])
    def xgboost():
        return controller.xgboost()

    @bp.route('/red-neuronal-lstm', methods=['POST'])
    def red_neuronal_lstm():
        return controller.red_neuronal_lstm()

    @bp.route('/predecir', methods=['GET'])
    def predecir():
        return controller.predecir()

    return bp