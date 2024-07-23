from mongoengine import connect

from src.reports.domain.repositores.estadistica_repository import CausaCount, EstadisticaData, EstadisticaRepository, TipoReporteCount
from src.database.model import EstadisticaReporte
from src.database.config import Config
from typing import List, Optional
from datetime import datetime

connect(host=Config.MONGO_URI)

class MongoEngineEstadisticaRepository(EstadisticaRepository):
    
    def _check_sufficient_data(self, min_observations: int = 60) -> bool:
        count = EstadisticaReporte.objects.count()
        return count >= min_observations

    def get_by_date_range(self, start_date: Optional[datetime], end_date: Optional[datetime]) -> List[EstadisticaData]:
        query = {}
        if start_date:
            query['fecha_creacion__gte'] = start_date
        if end_date:
            query['fecha_creacion__lte'] = end_date

        estadisticas = EstadisticaReporte.objects(**query)
        return [self._to_estadistica_data(est) for est in estadisticas]
        
    def save(self, estadistica: EstadisticaData) -> bool:
        try:
            mongo_estadistica = EstadisticaReporte(**estadistica)
            mongo_estadistica.save()
            return True
        except Exception as e:
            print(f"Error saving estadistica: {str(e)}")
            return False

    def get_count_by_tipo_reporte(self) -> List[TipoReporteCount]:
        if not self._check_sufficient_data():
            raise ValueError("Insufficient data for analysis. At least 60 observations are required.")
        
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
        if not self._check_sufficient_data():
            raise ValueError("Insufficient data for analysis. At least 60 observations are required.")
        
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