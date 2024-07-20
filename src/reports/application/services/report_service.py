import firebase_admin
from firebase_admin import credentials, storage
from src.reports.domain.repositores.estadistica_repository import EstadisticaRepository
from src.reports.infraestructure.repositories.MongoEngineReportRepository import MongoEngineReportRepository
from src.reports.application.services.pdf_services import create_pdf
from src.reports.application.services.nlp_service import NLPService

class ReportService:
    def __init__(self, report_repository, bucket):
        self.report_repository = report_repository
        self.estadistica_repository = EstadisticaRepository()
        self.nlp_service = NLPService(self.estadistica_repository)
        self.bucket = bucket

    def delete_all_reports(self):
        reports = self.get_all_reports()
        deleted_files_count = 0
        for report in reports:
            if report.pdf_url:
                blob_name = report.pdf_url.split('/')[-1]
                blob = self.bucket.blob(f'reports/{blob_name}')
                blob.delete()
                deleted_files_count += 1

            if report.imagen_url:
                image_blob_name = report.imagen_url.split('/')[-1]
                image_blob = self.bucket.blob(f'images/{image_blob_name}')
                image_blob.delete()
                deleted_files_count += 1

        deleted_db_count = self.report_repository.delete_all()
        
        return {
            'deleted_files': deleted_files_count,
            'deleted_db_records': deleted_db_count
        }
     
     
    def create_report(self, report_data, image_file):
        try:
            if not image_file:
                raise ValueError("No se proporcionó archivo de imagen")

            blob = self.bucket.blob(f'images/{image_file.filename}')
            blob.upload_from_file(image_file, content_type=image_file.content_type)
            blob.make_public()
            report_data['imagen_url'] = blob.public_url

            new_report = self.report_repository.create(report_data)

            estadistica = self.nlp_service.analizar_reporte(new_report)
            if estadistica is None:
                print("No se pudo crear la estadística del reporte")

            pdf, filename = create_pdf(new_report)

            pdf_blob = self.bucket.blob(f'reports/{filename}')
            pdf_blob.upload_from_string(pdf, content_type='application/pdf')
            pdf_blob.make_public()
            new_report.pdf_url = pdf_blob.public_url

            self.report_repository.update(new_report)

            return new_report
        except Exception as e:
            print(f"Error en create_report: {str(e)}")
            raise
        
    def get_report_by_id(self, report_id):
        return self.report_repository.get_by_id(report_id)

    def get_all_reports(self):
        return self.report_repository.get_all()

    def update_report(self, report_id, report_data):
        report = self.get_report_by_id(report_id)
        if report:
            for key, value in report_data.items():
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
    
