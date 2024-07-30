#report_Service
from firebase_admin import credentials, storage
from src.reports.domain.entities.estadistica_reporte import EstadisticaReporte
from src.reports.infraestructure.repositories.MongoEngineEstadisticaReporte import MongoEngineEstadisticaRepository
from src.reports.infraestructure.repositories.MongoEngineReportRepository import MongoEngineReportRepository
from src.reports.application.services.pdf_services import create_pdf
from src.reports.application.services.nlp_service import NLPService
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self, report_repository, bucket):
        self.report_repository = report_repository
        self.estadistica_repository = MongoEngineEstadisticaRepository()
        self.nlp_service = NLPService(self.estadistica_repository)
        self.bucket = bucket

    
     
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def create_report(self, report_data, image_file):
        try:
            print("Iniciando creación de reporte")
            if not image_file:
                raise ValueError("No se proporcionó archivo de imagen")

            print("Subiendo imagen al bucket")
            blob = self.bucket.blob(f'images/{image_file.filename}')
            blob.upload_from_file(image_file, content_type=image_file.content_type)
            blob.make_public()
            report_data['imagen_url'] = blob.public_url

            print("Creando nuevo reporte en la base de datos")
            report_data['estatus'] = 'pendiente' 
            new_report = self.report_repository.create(report_data)

            print("Analizando reporte")
            self.analizar_reporte(new_report)

            print("Creando PDF")
            pdf, filename = create_pdf(new_report)

            print("Subiendo PDF al bucket")
            pdf_blob = self.bucket.blob(f'reports/{filename}')
            pdf_blob.upload_from_string(pdf, content_type='application/pdf')
            pdf_blob.make_public()
            new_report.pdf_url = pdf_blob.public_url

            print("Actualizando reporte en la base de datos")
            self.report_repository.update(new_report)

            return new_report
        except Exception as e:
            print(f"Error en create_report: {str(e)}")
            raise


    def analizar_reporte(self, reporte):
        try:
            print("Inicio de análisis de reporte")
            descripcion = reporte['descripcion']
            tipo_reporte = reporte['tipo_reporte']
            fecha_creacion = reporte['fecha_creacion']
            print(f"Descripción: {descripcion}")
            print(f"Tipo de reporte: {tipo_reporte}")
            print(f"Fecha de creación: {fecha_creacion}")

            # Usar NLPService para extraer información
            causa, ubicacion, afectado = self.nlp_service.extraer_informacion(descripcion)
            print(f"Causa extraída: {causa}")
            print(f"Ubicación extraída: {ubicacion}")
            print(f"Afectado extraído: {afectado}")

            estadistica = {
                'causa': causa,
                'ubicacion': ubicacion,
                'afectado': afectado,
                'fecha_creacion': fecha_creacion,
                'tipo_reporte': tipo_reporte
            }

            self.estadistica_repository.save(estadistica)
            print("Reporte guardado en la base de datos")
            return "Reporte analizado y guardado con éxito."
        except Exception as e:
            print(f"Error en analizar_reporte: {str(e)}")
            return None
        
    def get_reports_for_charts(self):
        reports = self.get_all_reports()
        chart_data = []
        for report in reports:
            chart_data.append({
                'id': str(report.id),
                'titulo_reporte': report.titulo_reporte,
                'tipo_reporte': report.tipo_reporte,
                'fecha_creacion': report.fecha_creacion,
                # Agrega aquí cualquier otro campo que necesites para las gráficas
            })
        return chart_data
    
    def get_report_by_id(self, report_id):
        return self.report_repository.get_by_id(report_id)

    def get_all_reports(self):
        return self.report_repository.get_all()

    def update_report(self, report_id, report_data):
        report = self.get_report_by_id(report_id)
        if report:
            for key, value in report_data.items():
                if key == 'estatus':
                    
                    valid_statuses = ['pendiente', 'en_proceso', 'completado', 'cancelado']
                    if value not in valid_statuses:
                        raise ValueError(f"Estatus inválido: {value}")
                setattr(report, key, value)
            return self.report_repository.update(report)
        return None

    def delete_report(self, report_id):
        return self.report_repository.delete(report_id)

    def get_pdf(self, report_id):
        report = self.get_report_by_id(report_id)
        if report and report.pdf_url:
            blob = self.bucket.blob(report.pdf_url.split('/')[-1])
            return blob.download_as_bytes()
        return None

    def get_all_pdfs(self):
        reports = self.get_all_reports()
        pdfs = []
        for report in reports:
            if report.pdf_url:
                pdfs.append({
                    'id': report.id,
                    'title': report.titulo_reporte,
                    'pdf_url': report.pdf_url
                })
        return pdfs
    
    def get_pdf_reports(self):
        reports = self.report_repository.get_all()
        return [{'titulo_reporte': report.titulo_reporte, 'pdf_url': report.pdf_url} 
                for report in reports if report.pdf_url]
        
    def generate_time_series_chart(self, start_date=None, end_date=None):
        return self.chart_service.generar_serie_tiempo(start_date, end_date)

    def generate_pie_chart(self):
        return self.chart_service.generar_grafico_circular_tipos()

    def get_statistics_by_category(self, category):
        return self.estadistica_repository.get_by_categoria(category)

    def get_report_count_by_type(self):
        return self.estadistica_repository.get_count_by_tipo_reporte()
   
    def get_pdf_list(self):
        return self.report_repository.get_pdf_list()
    
    def delete_all_reports(self):
        reports = self.get_all_reports()
        deleted_files_count = 0
        errors = []

        for report in reports:
            if report.pdf_url:
                blob_name = report.pdf_url.split('/')[-1]
                blob = self.bucket.blob(f'reports/{blob_name}')
                try:
                    blob.delete()
                    deleted_files_count += 1
                except Exception as e:
                    errors.append(f"Error deleting PDF file: {str(e)}")

            if report.imagen_url:
                image_blob_name = report.imagen_url.split('/')[-1]
                image_blob = self.bucket.blob(f'images/{image_blob_name}')
                try:
                    image_blob.delete()
                    deleted_files_count += 1
                except Exception as e:
                    errors.append(f"Error deleting image file: {str(e)}")

        deleted_db_count = self.report_repository.delete_all()
        
        return {
            'deleted_files': deleted_files_count,
            'deleted_db_records': deleted_db_count,
            'errors': errors
        }
    
    def update_status(self, report_id, new_status):
        try:
            report = self.get_report_by_id(report_id)
            if report:
                valid_statuses = ['pendiente', 'en_proceso', 'completado', 'cancelado']
                if new_status not in valid_statuses:
                    raise ValueError(f"Estatus inválido: {new_status}")
                
                report.estatus = new_status
                updated_report = self.report_repository.update(report)
                return updated_report
            return None
        except Exception as e:
            print(f"Error updating report status: {str(e)}")
            raise

    
