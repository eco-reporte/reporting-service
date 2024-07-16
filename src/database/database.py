from src.database.config import Config

def get_db():
    client = Config.init_db()
    if client:
        return client.get_default_database()
    return None
