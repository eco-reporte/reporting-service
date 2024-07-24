from flask import request, jsonify, send_file
from io import BytesIO

class StatisticsController:
    def __init__(self, statistics_service):
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

    def get_time_series_analysis(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        try:
            chart_bytes = self.statistics_service.generate_time_series_analysis(start_date, end_date)
            return send_file(
                BytesIO(chart_bytes),
                mimetype='image/png',
                as_attachment=True,
                download_name='time_series_analysis.png'
            )
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Se produjo un error inesperado al generar el análisis de series temporales'}), 500

    def regresion_lineal_multiple(self):
        try:
            columna_objetivo = request.args.get('columna_objetivo', default='tipo_reporte')
            resultados = self.statistics_service.regresion_lineal_multiple(columna_objetivo)
            return jsonify(resultados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def descomposicion_clasica(self):
        try:
            columna_objetivo = request.args.get('columna_objetivo', default='tipo_reporte')
            resultados = self.statistics_service.descomposicion_clasica(columna_objetivo)
            return jsonify(resultados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def descomposicion_stl(self):
        try:
            columna_objetivo = request.args.get('columna_objetivo', default='tipo_reporte')
            resultados = self.statistics_service.descomposicion_stl(columna_objetivo)
            return jsonify(resultados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def suavizado_exponencial(self):
        try:
            columna_objetivo = request.args.get('columna_objetivo', default='tipo_reporte')
            resultados = self.statistics_service.suavizado_exponencial(columna_objetivo)
            return jsonify(resultados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def random_forest(self):
        try:
            columna_objetivo = request.args.get('columna_objetivo', default='tipo_reporte')
            resultados = self.statistics_service.random_forest(columna_objetivo)
            return jsonify(resultados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def xgboost(self):
        try:
            columna_objetivo = request.args.get('columna_objetivo', default='tipo_reporte')
            resultados = self.statistics_service.xgboost(columna_objetivo)
            return jsonify(resultados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def red_neuronal_lstm(self):
        try:
            columna_objetivo = request.args.get('columna_objetivo', default='tipo_reporte')
            resultados = self.statistics_service.red_neuronal_lstm(columna_objetivo)
            return jsonify(resultados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def predecir(self):
        try:
            modelo = request.args.get('modelo')
            causa = request.args.get('causa')
            ubicacion = request.args.get('ubicacion')
            afectado = request.args.get('afectado')
            
            if not all([modelo, causa, ubicacion, afectado]):
                return jsonify({'error': 'Faltan parámetros requeridos'}), 400
            
            prediccion = self.statistics_service.predecir(modelo, causa, ubicacion, afectado)
            return jsonify({'prediccion': float(prediccion)}), 200
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500