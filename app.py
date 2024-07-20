import sys
import os
import firebase_admin
from flask import Flask
from firebase_admin import credentials, storage
from src.database.config import Config
from src.reports.infraestructure.repositories.MongoEngineReportRepository import MongoEngineReportRepository
from src.reports.application.services.report_service import ReportService
from src.reports.infraestructure.controllers.report_controller import ReportController

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Flask application configuration
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Firebase
cred = credentials.Certificate('src/database/firebase_config.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'eco-reporte.appspot.com'
})
bucket = storage.bucket()

# Initialize services and controllers
report_repository = MongoEngineReportRepository()
report_service = ReportService(report_repository, bucket)
report_controller = ReportController(report_service)

from src.reports.infraestructure.routes.report_routes import create_report_blueprint
from src.reports.infraestructure.routes.statistics_routes import bp as statistics_routes_blueprint

report_routes_blueprint = create_report_blueprint(report_service, report_controller)
app.register_blueprint(report_routes_blueprint, url_prefix='/reports')
app.register_blueprint(statistics_routes_blueprint, url_prefix='/statistics')

if __name__ == '__main__':
    app.run(debug=True)
