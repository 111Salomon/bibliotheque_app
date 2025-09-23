from aifc import Error
from config.database import Database

class BaseModel:
    def __init__(self):
        self.db = Database()
        self.table_name = None
    
    def execute_query(self, query, params=None, fetch=False):
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                if 'SELECT' in query.upper():
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
            else:
                connection.commit()
                # For INSERT queries cursor.lastrowid will be the new id (truthy)
                # For UPDATE/DELETE lastrowid is usually 0; use rowcount to indicate affected rows
                last_id = getattr(cursor, 'lastrowid', None)
                if last_id:
                    result = last_id
                else:
                    # rowcount will be number of affected rows (0 if none)
                    result = getattr(cursor, 'rowcount', 0)
            
            cursor.close()
            return result
        except Error as e:
            print(f"Erreur SQL: {e}")
            return None
    
    def find_all(self):
        query = f"SELECT * FROM {self.table_name} ORDER BY id"
        return self.execute_query(query, fetch=True)
    
    def find_by_id(self, id):
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        result = self.execute_query(query, (id,), fetch=True)
        return result[0] if result else None
    
    def delete(self, id):
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        return self.execute_query(query, (id,))