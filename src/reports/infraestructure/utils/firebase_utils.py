import firebase_admin
from firebase_admin import credentials, storage
import os

class FirebaseUtils:
    def __init__(self, firebase_config_path, storage_bucket):
        self.cred = credentials.Certificate(firebase_config_path)
        firebase_admin.initialize_app(self.cred, {'storageBucket': storage_bucket})
        self.bucket = storage.bucket()

    def upload_file(self, local_file_path, firebase_file_path):
        blob = self.bucket.blob(firebase_file_path)
        blob.upload_from_filename(local_file_path)
        blob.make_public()
        return blob.public_url

    def download_file(self, firebase_file_path, local_file_path):
        blob = self.bucket.blob(firebase_file_path)
        blob.download_to_filename(local_file_path)
