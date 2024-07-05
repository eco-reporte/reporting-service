import firebase_admin
from firebase_admin import credentials, storage
from src.reports.application.services.pdf_services import create_pdf

class ReportService:
    def __init__(self, report_repository):
        self.report_repository = report_repository

        # Inicializar Firebase Admin SDK
        cred = credentials.Certificate('src/database/firebase_config.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'eco-reporte.appspot.com'
        })

    def create_report(self, report_data, image_file):
        # Subir imagen a Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'images/{image_file.filename}')
        blob.upload_from_file(image_file)
        blob.make_public()
        report_data['imagen_url'] = blob.public_url

        # Crear reporte en la base de datos
        new_report = self.report_repository.create(report_data)

        # Crear PDF
        pdf, filename = create_pdf(new_report)

        # Subir PDF a Firebase Storage
        pdf_blob = bucket.blob(f'reports/{filename}')
        pdf_blob.upload_from_string(pdf, content_type='application/pdf')
        pdf_blob.make_public()
        new_report.pdf_url = pdf_blob.public_url

        # Actualizar reporte con la URL del PDF
        self.report_repository.update(new_report)

        return new_report
    
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
            bucket = storage.bucket()
            blob = bucket.blob(report.pdf_url.split('/')[-1])
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
                    'pdf_url': report.pdf_url  # Esta es la URL completa de Firebase
                })
        return pdfs
