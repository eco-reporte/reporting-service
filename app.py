from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database.database import init_db

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'  # Cambiar según tus credenciales
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la extensión SQLAlchemy
db = SQLAlchemy(app)

# Inicialización de la base de datos
init_db(app)

# Importar rutas después de inicializar db para evitar ciclos de importación
from reports.infrastructure.routes.report_routes import bp as report_routes_blueprint

# Registro de Blueprints (rutas)
app.register_blueprint(report_routes_blueprint)

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
