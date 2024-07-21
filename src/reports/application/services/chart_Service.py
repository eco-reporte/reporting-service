#chart_service
import matplotlib.pyplot as plt
from io import BytesIO

from reports.domain.repositores.estadistica_repository import EstadisticaRepository
class ChartService:
    def __init__(self, estadistica_repository: EstadisticaRepository):
        self.estadistica_repository = estadistica_repository

    def generar_serie_tiempo(self, start_date=None, end_date=None):
        if start_date and end_date:
            estadisticas = self.estadistica_repository.get_by_date_range(start_date, end_date)
        else:
            estadisticas = self.estadistica_repository.get_all()
        
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
        buf.seek(0)
        plt.close()

        return buf

    def generar_grafico_circular_tipos(self):
        tipos = self.estadistica_repository.get_count_by_tipo_reporte()
        labels = [tipo['_id'] for tipo in tipos]
        sizes = [tipo['count'] for tipo in tipos]

        plt.figure(figsize=(10, 10))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Distribución de tipos de reportes')

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf