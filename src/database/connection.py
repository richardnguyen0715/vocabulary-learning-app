from pymongo import MongoClient
import config

class DatabaseConnection:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(config.DATABASE_URI)
        self.db = self.client[config.DATABASE_NAME]

    def close(self):
        if self.client:
            self.client.close()
            
def connect_to_database():
    db_connection = DatabaseConnection()
    db_connection.connect()
    print("Connected to the database")
    return db_connection