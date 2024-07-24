# src/reports/application/services/StatisticsService.py

from io import BytesIO
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from src.reports.application.services.chart_Service import ChartService
from src.reports.domain.repositores.estadistica_repository import EstadisticaRepository
from statsmodels.tsa.seasonal import seasonal_decompose
from typing import List, Dict
from datetime import datetime, timedelta

class StatisticsService:
    
    def __init__(self, estadistica_repository: EstadisticaRepository, chart_service: ChartService):
        self.estadistica_repository = estadistica_repository
        self.chart_service = chart_service
        self.models = {}

    def preparar_datos(self, columna_objetivo='tipo_reporte'):
        datos = self.estadistica_repository.get_all()
        df = pd.DataFrame(datos)
        
        # Convertir fecha_creacion a datetime
        df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
        
        # Codificar variables categóricas
        le = LabelEncoder()
        for col in ['causa', 'ubicacion', 'afectado', columna_objetivo]:
            df[col] = le.fit_transform(df[col])
        
        return df

    def regresion_lineal_multiple(self, columna_objetivo='tipo_reporte'):
        df = self.preparar_datos(columna_objetivo)
        
        X = df[['causa', 'ubicacion', 'afectado']]
        y = df[columna_objetivo]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        modelo = LinearRegression()
        modelo.fit(X_train, y_train)
        
        self.models['regresion_lineal'] = modelo
        
        return {
            'r2_score': modelo.score(X_test, y_test),
            'coeficientes': dict(zip(X.columns, modelo.coef_))
        }

    def descomposicion_clasica(self, columna_objetivo='tipo_reporte'):
        df = self.preparar_datos(columna_objetivo)
        df = df.set_index('fecha_creacion').resample('D')[columna_objetivo].mean().fillna(method='ffill')
        
        resultado = seasonal_decompose(df, model='additive')
        
        return {
            'tendencia': resultado.trend.tolist(),
            'estacionalidad': resultado.seasonal.tolist(),
            'residual': resultado.resid.tolist()
        }

    def descomposicion_stl(self, columna_objetivo='tipo_reporte'):
        df = self.preparar_datos(columna_objetivo)
        df = df.set_index('fecha_creacion').resample('D')[columna_objetivo].mean().fillna(method='ffill')
        
        resultado = seasonal_decompose(df, model='additive', extrapolate_trend='freq')
        
        return {
            'tendencia': resultado.trend.tolist(),
            'estacionalidad': resultado.seasonal.tolist(),
            'residual': resultado.resid.tolist()
        }

    
    def random_forest(self, columna_objetivo='tipo_reporte'):
        df = self.preparar_datos(columna_objetivo)
        
        X = df[['causa', 'ubicacion', 'afectado']]
        y = df[columna_objetivo]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        modelo = RandomForestRegressor(n_estimators=100, random_state=42)
        modelo.fit(X_train, y_train)
        
        self.models['random_forest'] = modelo
        
        return {
            'r2_score': modelo.score(X_test, y_test),
            'importancia_caracteristicas': dict(zip(X.columns, modelo.feature_importances_))
        }

    def xgboost(self, columna_objetivo='tipo_reporte'):
        df = self.preparar_datos(columna_objetivo)
        
        X = df[['causa', 'ubicacion', 'afectado']]
        y = df[columna_objetivo]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        modelo = XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
        modelo.fit(X_train, y_train)
        
        self.models['xgboost'] = modelo
        
        return {
            'r2_score': modelo.score(X_test, y_test),
            'importancia_caracteristicas': dict(zip(X.columns, modelo.feature_importances_))
        }

    
    def predecir(self, modelo, causa: str, ubicacion: str, afectado: str):
        if modelo not in self.models:
            raise ValueError(f"El modelo '{modelo}' no ha sido entrenado.")
        
        le = LabelEncoder()
        datos_entrada = pd.DataFrame({
            'causa': le.fit_transform([causa]),
            'ubicacion': le.fit_transform([ubicacion]),
            'afectado': le.fit_transform([afectado])
        })
        
        prediccion = self.models[modelo].predict(datos_entrada)
        
        return prediccion[0]
    
    
    # def __init__(self, estadistica_repository: EstadisticaRepository, chart_service: ChartService):
    #     self.estadistica_repository = estadistica_repository
    #     self.chart_service = chart_service

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
        
        # Si no se proporciona una fecha de inicio, use los últimos 90 días
        if not start:
            start = end - timedelta(days=90) if end else datetime.now() - timedelta(days=90)
        
        # Si no se proporciona una fecha de fin, use la fecha actual
        if not end:
            end = datetime.now()
        
        data = self.estadistica_repository.get_by_date_range(start, end)
        
        df = pd.DataFrame(data)
        
        if 'fecha_creacion' not in df.columns:
            raise ValueError("No se encontró la columna 'fecha_creacion' en los datos")
        
        df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
        df.set_index('fecha_creacion', inplace=True)
        df = df.sort_index()
        
        df['count'] = 1  # Asume que cada fila representa un evento
        df = df.resample('D')['count'].sum().fillna(0)
        
        # Asegúrate de tener al menos 60 observaciones
        if len(df) < 60:
            raise ValueError(f"Se requieren al menos 60 observaciones para el análisis. Solo hay {len(df)} observaciones.")
        
        # Ajusta el período según la cantidad de datos disponibles
        period = min(30, len(df) // 2)  # Usa la mitad de la longitud de los datos, máximo 30
        
        result = seasonal_decompose(df, model='additive', period=period)

        return self.chart_service.generar_analisis_serie_tiempo(result)