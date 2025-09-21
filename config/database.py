import mysql.connector
from mysql.connector import Error

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.host = 'localhost'
            self.database = 'bibliotheque'
            self.user = 'root'  
            self.password = ''  
            self.connection = None
            self.initialized = True
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connexion à MySQL réussie")
        except Error as e:
            print(f"Erreur de connexion à MySQL: {e}")
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connexion MySQL fermée")
    
    def get_connection(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection