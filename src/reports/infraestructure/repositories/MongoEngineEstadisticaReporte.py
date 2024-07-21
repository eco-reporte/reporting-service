from mongoengine import connect
from src.database.model import EstadisticaReporte
from src.database.config import Config
from src.reports.domain.repositores.estadistica_repository import EstadisticaRepository, EstadisticaData, TipoReporteCount, CausaCount
from typing import List, Optional
from datetime import datetime

connect(host=Config.MONGO_URI)

class MongoEngineEstadisticaRepository(EstadisticaRepository):
    def save(self, estadistica: EstadisticaData) -> bool:
        try:
            mongo_estadistica = EstadisticaReporte(**estadistica)
            mongo_estadistica.save()
            return True
        except Exception as e:
            print(f"Error saving estadistica: {str(e)}")
            return False

    def get_count_by_tipo_reporte(self) -> List[TipoReporteCount]:
        try:
            pipeline = [
                {'$group': {'_id': '$tipo_reporte', 'count': {'$sum': 1}}},
                {'$match': {'_id': {'$ne': None}}}
            ]
            return list(EstadisticaReporte.objects.aggregate(*pipeline))
        except Exception as e:
            print(f"Error getting count by tipo_reporte: {str(e)}")
            return []

    def get_top_causas(self, top_n: int) -> List[CausaCount]:
        try:
            pipeline = [
                {'$group': {'_id': '$causa', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': top_n}
            ]
            return list(EstadisticaReporte.objects.aggregate(*pipeline))
        except Exception as e:
            print(f"Error getting top causas: {str(e)}")
            return []

    def get_by_categoria(self, categoria: str) -> List[EstadisticaData]:
        try:
            return [self._to_estadistica_data(est) for est in EstadisticaReporte.objects(causa=categoria)]
        except Exception as e:
            print(f"Error getting estadisticas by categoria: {str(e)}")
            return []

    def get_all(self) -> List[EstadisticaData]:
        try:
            return [self._to_estadistica_data(est) for est in EstadisticaReporte.objects()]
        except Exception as e:
            print(f"Error getting all estadisticas: {str(e)}")
            return []

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[EstadisticaData]:
        try:
            return [self._to_estadistica_data(est) for est in EstadisticaReporte.objects(fecha_creacion__gte=start_date, fecha_creacion__lte=end_date)]
        except Exception as e:
            print(f"Error getting estadisticas by date range: {str(e)}")
            return []

    def update(self, id: str, estadistica: EstadisticaData) -> bool:
        try:
            EstadisticaReporte.objects(id=id).update_one(**estadistica)
            return True
        except Exception as e:
            print(f"Error updating estadistica: {str(e)}")
            return False

    def delete(self, id: str) -> bool:
        try:
            EstadisticaReporte.objects(id=id).delete()
            return True
        except Exception as e:
            print(f"Error deleting estadistica: {str(e)}")
            return False

    def get_by_id(self, id: str) -> Optional[EstadisticaData]:
        try:
            est = EstadisticaReporte.objects(id=id).first()
            return self._to_estadistica_data(est) if est else None
        except Exception as e:
            print(f"Error getting estadistica by id: {str(e)}")
            return None

    def _to_estadistica_data(self, est: EstadisticaReporte) -> EstadisticaData:
        return EstadisticaData(
            id=str(est.id),
            causa=est.causa,
            ubicacion=est.ubicacion,
            afectado=est.afectado,
            fecha_creacion=est.fecha_creacion,
            tipo_reporte=est.tipo_reporte
        )