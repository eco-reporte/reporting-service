from pymongo import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect

class Config:
    MONGO_URI = "mongodb+srv://203406:tNMzgtP0j4gOGM4A@reporting-service.3t3jftc.mongodb.net/db_eco_reporte?retryWrites=true&w=majority&appName=reporting-service"

    @staticmethod
    def init_db():
        try:
            # Configurar MongoEngine
            connect(host=Config.MONGO_URI)
            
            # También puedes mantener la conexión de PyMongo si la necesitas
            client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return client
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return None