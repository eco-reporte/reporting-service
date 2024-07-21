from abc import ABC, abstractmethod
from typing import List, Dict, TypedDict, Optional
from datetime import datetime

class TipoReporteCount(TypedDict):
    _id: str
    count: int

class CausaCount(TypedDict):
    _id: str
    count: int

class EstadisticaData(TypedDict):
    id: str
    causa: str
    ubicacion: str
    afectado: str
    fecha_creacion: datetime
    tipo_reporte: str

class EstadisticaRepository(ABC):
    @abstractmethod
    def get_count_by_tipo_reporte(self) -> List[TipoReporteCount]:
        pass

    @abstractmethod
    def get_top_causas(self, top_n: int) -> List[CausaCount]:
        pass

    @abstractmethod
    def get_all(self) -> List[EstadisticaData]:
        pass

    @abstractmethod
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[EstadisticaData]:
        pass

    @abstractmethod
    def get_by_categoria(self, categoria: str) -> List[EstadisticaData]:
        pass

    @abstractmethod
    def save(self, estadistica: EstadisticaData) -> bool:
        pass

    @abstractmethod
    def update(self, id: str, estadistica: EstadisticaData) -> bool:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[EstadisticaData]:
        pass