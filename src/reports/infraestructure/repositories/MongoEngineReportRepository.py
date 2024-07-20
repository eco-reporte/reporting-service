from mongoengine import connect
from src.database.model import Reporte
from src.database.config import Config

# Establecer la conexión a MongoDB al iniciar la aplicación
connect(host=Config.MONGO_URI)

class MongoEngineReportRepository:
    def __init__(self):
        pass

    def create(self, report_data):
        try:
            report = Reporte(**report_data)
            report.save()
            return report
        except Exception as e:
            print(f"Error creating report: {str(e)}")
            raise

    def update(self, report):
        try:
            report.save()
            return report
        except Exception as e:
            print(f"Error updating report: {e}")
            return None

    def delete(self, report_id):
        try:
            report = self.get_by_id(report_id)
            if report:
                report.delete()
            return report
        except Exception as e:
            print(f"Error deleting report: {e}")
            return None

    def get_by_id(self, report_id):
        try:
            return Reporte.objects(id=report_id).first()
        except Exception as e:
            print(f"Error getting report by id: {e}")
            return None

    def get_all(self):
        try:
            return list(Reporte.objects())
        except Exception as e:
            print(f"Error getting all reports: {e}")
            return []

    def get_all_pdf_urls(self):
        try:
            return [report.pdf_url for report in Reporte.objects() if report.pdf_url]
        except Exception as e:
            print(f"Error getting PDF URLs: {e}")
            return []

    def delete_all(self):
        try:
            return Reporte.objects().delete()
        except Exception as e:
            print(f"Error deleting all reports: {e}")
            return 0
        
    def get_pdf_list(self):
        try:
            return [{"id": str(report.id), "pdf_url": report.pdf_url, "titulo_reporte": report.titulo_reporte} 
                    for report in Reporte.objects() if hasattr(report, 'pdf_url') and report.pdf_url]
        except Exception as e:
            print(f"Error getting PDF list: {e}")
            return []