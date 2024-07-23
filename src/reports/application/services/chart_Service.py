import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib
matplotlib.use('Agg')


from src.reports.domain.repositores.estadistica_repository import EstadisticaRepository

class ChartService:
    def __init__(self, estadistica_repository: EstadisticaRepository):
        self.estadistica_repository = estadistica_repository

    def generar_serie_tiempo(self, estadisticas) -> bytes:
        fechas = [est.fecha_creacion for est in estadisticas]
        fechas.sort()

        plt.figure(figsize=(12, 6))
        plt.plot(fechas, range(len(fechas)))
        plt.title('Número acumulado de reportes a lo largo del tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('Número de reportes')
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        return buf.getvalue()

    def generar_grafico_circular_tipos(self, tipos) -> bytes:
        labels = [tipo['_id'] for tipo in tipos]
        sizes = [tipo['count'] for tipo in tipos]

        plt.figure(figsize=(10, 10))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Distribución de tipos de reportes')

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        return buf.getvalue()

    def generar_grafico_barras_causas(self, causas) -> bytes:
        labels = [causa['_id'] for causa in causas]
        values = [causa['count'] for causa in causas]

        plt.figure(figsize=(12, 6))
        plt.bar(labels, values)
        plt.title('Top Causas de Reportes')
        plt.xlabel('Causa')
        plt.ylabel('Número de reportes')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        return buf.getvalue()
    
    def generar_analisis_serie_tiempo(self, result) -> bytes:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 16))
        
        result.observed.plot(ax=ax1)
        ax1.set_title('Observado')
        result.trend.plot(ax=ax2)
        ax2.set_title('Tendencia')
        result.seasonal.plot(ax=ax3)
        ax3.set_title('Estacionalidad')
        result.resid.plot(ax=ax4)
        ax4.set_title('Residuos (Ruido)')

        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)

        return buf.getvalue()
    
    