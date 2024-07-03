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
