import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect

class Config:
    MONGO_URI = os.environ.get('MONGO_URI')
    @staticmethod
    def init_db():
        try:
            connect(host=Config.MONGO_URI)
            
            client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return client
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return None