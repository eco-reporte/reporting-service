# src/reports/application/services/StatisticsService.py

from io import BytesIO
from matplotlib import pyplot as plt
import pandas as pd
from src.reports.application.services.chart_Service import ChartService
from src.reports.domain.repositores.estadistica_repository import EstadisticaRepository
from statsmodels.tsa.seasonal import seasonal_decompose
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
    
    def generate_time_series_analysis(self, start_date: str, end_date: str) -> bytes:
        start = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        data = self.estadistica_repository.get_by_date_range(start, end)
        
        df = pd.DataFrame(data)
        
        if 'fecha_creacion' not in df.columns:
            raise ValueError("No se encontró la columna 'fecha_creacion' en los datos")
        
        df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
        df.set_index('fecha_creacion', inplace=True)
        df = df.sort_index()
        
        df['count'] = 1  # Asume que cada fila representa un evento
        df = df.resample('D')['count'].sum().fillna(0)
        
        result = seasonal_decompose(df, model='additive', period=30)  # Ajusta el período según tus datos

        return self.chart_service.generar_analisis_serie_tiempo(result)