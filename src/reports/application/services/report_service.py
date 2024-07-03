from reports.domain.repositores.report_repository import ReportRepository
import os
from firebase_admin import storage

class ReportService:
    def __init__(self, report_repository):
        self.report_repository = report_repository

    # def create_report(self, report_data):
    #     return self.report_repository.create(report_data)
    
    def create_report(self, report_data, image_file):
        # Subir imagen a Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'images/{image_file.filename}')
        blob.upload_from_file(image_file)
        blob.make_public()
        report_data['imagen_url'] = blob.public_url

        return self.report_repository.create(report_data)