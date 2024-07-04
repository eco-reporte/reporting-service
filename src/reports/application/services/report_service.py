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
