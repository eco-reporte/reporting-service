#analisis_service
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

from reports.domain.repositores.estadistica_repository import EstadisticaRepository

class AnalysisService:
    def __init__(self):
        self.estadistica_repository = EstadisticaRepository()

    def obtener_estadisticas(self):
        estadisticas = self.estadistica_repository.get_all()

        data = []
        for estadistica in estadisticas:
            data.append({
                'categoria': estadistica.categoria,
                'que_paso': estadistica.que_paso,
                'donde_paso': estadistica.donde_paso,
                'a_quien_paso': estadistica.a_quien_paso,
                'fecha': estadistica.fecha
            })
        df = pd.DataFrame(data)
        return df

    def generar_grafico_pie(self, df):
        conteo_categorias = df['categoria'].value_counts()

        plt.figure(figsize=(10, 7))
        plt.pie(conteo_categorias, labels=conteo_categorias.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Distribución de Causas de Reportes')

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf

def generar_serie_tiempo(self, df):
    df['fecha'] = pd.to_datetime(df['fecha'])

    series_tiempo = df.groupby([df['fecha'].dt.to_period('M'), 'categoria']).size().unstack(fill_value=0)

    plt.figure(figsize=(15, 8))
    series_tiempo.plot(kind='line')
    plt.title('Series de Tiempo de Causas de Reportes')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Reportes')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf


# Uso del servicio de análisis
analysis_service = AnalysisService()
df_estadisticas = analysis_service.obtener_estadisticas()
analysis_service.generar_grafico_pie(df_estadisticas)
analysis_service.generar_serie_tiempo(df_estadisticas)
