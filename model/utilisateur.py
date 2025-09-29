# 4. MODEL/UTILISATEUR.PY (Hérite de Personne)

from model.base_model import BaseModel
from model.personne import Personne

class Utilisateur(BaseModel, Personne):
    def __init__(self):
        BaseModel.__init__(self)
        Personne.__init__(self)
        self.table_name = "utilisateurs"
    
    def create(self, data):
        query = """
        INSERT INTO utilisateurs (nom, prenom, email, telephone)
        VALUES (%(nom)s, %(prenom)s, %(email)s, %(telephone)s)
        """
        return self.execute_query(query, data)
    
    def update(self, id, data):
        query = """
        UPDATE utilisateurs 
        SET nom=%(nom)s, prenom=%(prenom)s, email=%(email)s, telephone=%(telephone)s
        WHERE id=%(id)s
        """
        data['id'] = id
        return self.execute_query(query, data)
    
    def find_by_email(self, email):
        query = "SELECT * FROM utilisateurs WHERE email = %s"
        result = self.execute_query(query, (email,), fetch=True)
        return result[0] if result else None