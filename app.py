from flask import Flask
from flask_cors import CORS
import firebase_admin
import os
from firebase_admin import credentials, storage
from src.reports.application.services.StatisticsService import StatisticsService
from src.reports.application.services.chart_Service import ChartService
from src.reports.infraestructure.repositories.MongoEngineEstadisticaReporte import MongoEngineEstadisticaRepository
from src.database.config import Config
from src.reports.infraestructure.repositories.MongoEngineReportRepository import MongoEngineReportRepository
from src.reports.application.services.report_service import ReportService

from src.reports.infraestructure.controllers.report_controller import ReportController
from src.reports.infraestructure.controllers.statistics_controller import StatisticsController
from src.reports.infraestructure.routes.report_routes import create_report_blueprint
from src.reports.infraestructure.routes.statistics_routes import create_statistics_blueprint

# Flask application configuration
app = Flask(__name__)
CORS(app) 
app.config.from_object(Config)

# Initialize Firebase
firebase_config_path = os.getenv('FIREBASE_CONFIG_PATH', 'src/database/firebase_config.json')
cred = credentials.Certificate(firebase_config_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'eco-reporte.appspot.com'
})
bucket = storage.bucket()

# Initialize repositories
report_repository = MongoEngineReportRepository()
estadistica_repository = MongoEngineEstadisticaRepository()

# Initialize services
report_service = ReportService(report_repository, bucket)
chart_service = ChartService(estadistica_repository)
statistics_service = StatisticsService(estadistica_repository, chart_service)

# Initialize controllers
report_controller = ReportController(report_service)
statistics_controller = StatisticsController(statistics_service)

# Register blueprints
report_routes_blueprint = create_report_blueprint(report_service, report_controller)
app.register_blueprint(report_routes_blueprint, url_prefix='/reports')

statistics_routes_blueprint = create_statistics_blueprint(statistics_service)
app.register_blueprint(statistics_routes_blueprint, url_prefix='/statistics')

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3003))
    app.run(host="0.0.0.0", port=port, debug=True)