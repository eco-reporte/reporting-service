import sys
import os
from flask import Flask
from src.database.config import Config

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Flask application configuration
app = Flask(__name__)
app.config.from_object(Config)

# Database initialization
db_client = Config.init_db()
if db_client:
    db = db_client.get_database('db_eco_reporte')
else:
    print("Failed to initialize the database. Exiting.")
    sys.exit(1)

# Import and register routes
from src.reports.infraestructure.routes.report_routes import bp as report_routes_blueprint
app.register_blueprint(report_routes_blueprint)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
