
from model.base_model import BaseModel

class Livre(BaseModel):
    def __init__(self):
        super().__init__()
        self.table_name = "livres"
    
    def create(self, data):
        query = """
        INSERT INTO livres (titre, auteur, isbn, genre, annee_publication)
        VALUES (%(titre)s, %(auteur)s, %(isbn)s, %(genre)s, %(annee_publication)s)
        """
        return self.execute_query(query, data)
    
    def update(self, id, data):
        query = """
        UPDATE livres 
        SET titre=%(titre)s, auteur=%(auteur)s, isbn=%(isbn)s, 
            genre=%(genre)s, annee_publication=%(annee_publication)s
        WHERE id=%(id)s
        """
        data['id'] = id
        return self.execute_query(query, data)
    
    def find_disponibles(self):
        query = "SELECT * FROM livres WHERE disponible = TRUE"
        return self.execute_query(query, fetch=True)