from src.reports.application.services.chart_Service import ChartService
from src.reports.domain.repositores.estadistica_repository import EstadisticaRepository

from typing import List, Dict
from datetime import datetime

class StatisticsService:
    def __init__(self, estadistica_repository: EstadisticaRepository, chart_service: ChartService):
        self.estadistica_repository = estadistica_repository
        self.chart_service = chart_service

    def get_report_count_by_type(self) -> List[Dict[str, int]]:
        return self.estadistica_repository.get_count_by_tipo_reporte()

    def get_statistics_by_category(self, category: str) -> List[Dict]:
        return self.estadistica_repository.get_by_categoria(category)

    def get_top_causes(self, top_n: int) -> List[Dict[str, int]]:
        return self.estadistica_repository.get_top_causas(top_n)

    def generate_pie_chart(self) -> bytes:
        data = self.get_report_count_by_type()
        return self.chart_service.generar_grafico_circular_tipos(data)

    def generate_time_series_chart(self, start_date: str, end_date: str) -> bytes:
        start = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        data = self.estadistica_repository.get_by_date_range(start, end)
        return self.chart_service.generar_serie_tiempo(data)

    def generate_bar_chart(self) -> bytes:
        data = self.get_top_causes(10)  # Top 10 causes
        return self.chart_service.generar_grafico_barras_causas(data)