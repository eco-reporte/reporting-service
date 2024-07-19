from src.reports.domain.entities.estadistica_reporte import EstadisticaReporte

class EstadisticaRepository:
    def save(self, estadistica_reporte: EstadisticaReporte):
        estadistica_reporte.save()
        return estadistica_reporte

    def get_all(self):
        return EstadisticaReporte.objects.all()

    def get_by_categoria(self, categoria):
        return EstadisticaReporte.objects(categoria=categoria).all()

    def get_by_date_range(self, start_date, end_date):
        return EstadisticaReporte.objects(fecha_creacion__gte=start_date, fecha_creacion__lte=end_date).all()

    def get_count_by_tipo_reporte(self):
        pipeline = [
            {"$group": {"_id": "$tipo_reporte", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return EstadisticaReporte.objects.aggregate(pipeline)