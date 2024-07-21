from mongoengine import connect
from src.database.model import EstadisticaReporte
from src.database.estadisticasModel import EstadisticaReporte
from src.database.config import Config

# Establecer la conexión a MongoDB al iniciar la aplicación
connect(host=Config.MONGO_URI)

class MongoEngineEstadisticaRepository:
    def __init__(self):
        pass

    def save(self, estadistica):
        try:
            mongo_estadistica = EstadisticaReporte(
                causa=estadistica.causa,
                ubicacion=estadistica.ubicacion,
                afectado=estadistica.afectado,
                fecha_creacion=estadistica.fecha_creacion,
                tipo_reporte=estadistica.tipo_reporte
            )
            mongo_estadistica.save()
            return True
        except Exception as e:
            print(f"Error saving estadistica: {str(e)}")
            return False

    def get_count_by_tipo_reporte(self):
        try:
            print("Iniciando get_count_by_tipo_reporte")
            print(f"Total documentos en la colección: {EstadisticaReporte.objects.count()}")
            
            # Imprimir algunos documentos de muestra
            sample_docs = list(EstadisticaReporte.objects[:5])
            print(f"Muestra de documentos: {sample_docs}")
            
            pipeline = [
                {
                    '$group': {
                        '_id': '$tipo_reporte',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$match': {
                        '_id': {'$ne': None}
                    }
                }
            ]
            result = list(EstadisticaReporte.objects.aggregate(*pipeline))
            print(f"Aggregation result: {result}")
            return result
        except Exception as e:
            print(f"Error getting count by tipo_reporte: {str(e)}")
            return []

    def get_by_categoria(self, categoria):
        try:
            return list(EstadisticaReporte.objects(causa=categoria))
        except Exception as e:
            print(f"Error getting estadisticas by categoria: {str(e)}")
            return []

    def get_all(self):
        try:
            return list(EstadisticaReporte.objects())
        except Exception as e:
            print(f"Error getting all estadisticas: {str(e)}")
            return []