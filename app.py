import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask
from database.config import Config
from database.database import db, init_db

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicialización de la extensión SQLAlchemy
init_db(app)

# Crear las tablas de la base de datos
with app.app_context():
    db.create_all()

# Importar rutas después de inicializar db para evitar ciclos de importación
from reports.infraestructure.routes.report_routes import bp as report_routes_blueprint

# Registro de Blueprints (rutas)
app.register_blueprint(report_routes_blueprint)

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)