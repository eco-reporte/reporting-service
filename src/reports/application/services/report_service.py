# reports/application/services/report_service.py

import firebase_admin
from firebase_admin import credentials, storage

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
        return self.report_repository.create(report_data)

    def upload_pdf_to_firebase(self, pdf_data, filename):
        # Subir PDF a Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'pdfs/{filename}')
        blob.upload_from_string(pdf_data, content_type='application/pdf')
        blob.make_public()
        return blob.public_url
    
    def update_report(self, report):
        # Actualizar el reporte en la base de datos
        self.report_repository.update(report)

    def delete_report(self, report_id):
        return self.report_repository.delete(report_id)

    def get_report_by_id(self, report_id):
        return self.report_repository.get_by_id(report_id)

    def get_all_reports(self):
        return self.report_repository.get_all()
