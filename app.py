import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
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

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verificación de variables de entorno
logger.info(f"FIREBASE_TYPE: {os.getenv('FIREBASE_TYPE')}")
logger.info(f"FIREBASE_PROJECT_ID: {os.getenv('FIREBASE_PROJECT_ID')}")
# No incluyas la clave privada en los logs por seguridad

# Verificación de configuración de Firebase
if os.path.exists('src/database/firebase_config.json'):
    logger.info("Firebase config file found.")
else:
    logger.error("Firebase config file not found.")

# Configuración de Firebase
firebase_config = {
    "type": os.getenv('FIREBASE_TYPE'),
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
    "universe_domain": os.getenv('FIREBASE_UNIVERSE_DOMAIN')
}

# Configuración de la aplicación Flask
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Inicialización de Firebase
logger.info("Initializing Firebase...")
try:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'eco-reporte.appspot.com'
    })
    bucket = storage.bucket()
    logger.info("Firebase initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Firebase: {str(e)}")
    raise

# Inicialización de repositorios
logger.info("Initializing repositories...")
try:
    report_repository = MongoEngineReportRepository()
    estadistica_repository = MongoEngineEstadisticaRepository()
    logger.info("Repositories initialized successfully")
except Exception as e:
    logger.error(f"Error initializing repositories: {str(e)}")
    raise

# Inicialización de servicios
logger.info("Initializing services...")
try:
    report_service = ReportService(report_repository, bucket)
    chart_service = ChartService(estadistica_repository)
    statistics_service = StatisticsService(estadistica_repository, chart_service)
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing services: {str(e)}")
    raise

# Inicialización de controladores
logger.info("Initializing controllers...")
try:
    report_controller = ReportController(report_service)
    statistics_controller = StatisticsController(statistics_service)
    logger.info("Controllers initialized successfully")
except Exception as e:
    logger.error(f"Error initializing controllers: {str(e)}")
    raise

# Registro de blueprints
logger.info("Registering blueprints...")
try:
    report_routes_blueprint = create_report_blueprint(report_service, report_controller)
    app.register_blueprint(report_routes_blueprint, url_prefix='/reports')

    statistics_routes_blueprint = create_statistics_blueprint(statistics_service)
    app.register_blueprint(statistics_routes_blueprint, url_prefix='/statistics')
    logger.info("Blueprints registered successfully")
except Exception as e:
    logger.error(f"Error registering blueprints: {str(e)}")
    raise

# Manejador de errores global
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled Exception: {str(e)}")
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
