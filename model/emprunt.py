from model.base_model import BaseModel

class Emprunt(BaseModel):
    def __init__(self):
        super().__init__()
        self.table_name = "emprunts"
    
    def create(self, data):
        """Créer un emprunt et marquer le livre comme indisponible"""
        query = """
        INSERT INTO emprunts (utilisateur_id, livre_id, date_retour_prevue)
        VALUES (%(utilisateur_id)s, %(livre_id)s, %(date_retour_prevue)s)
        """
        result = self.execute_query(query, data)
        
        # Marquer le livre comme indisponible
        if result:
            update_book = "UPDATE livres SET disponible = FALSE WHERE id = %(livre_id)s"
            self.execute_query(update_book, {'livre_id': data['livre_id']})
        
        return result
    
    def update(self, id, data):
        """Mettre à jour un emprunt"""
        query = """
        UPDATE emprunts 
        SET date_retour_effective=%(date_retour_effective)s, statut=%(statut)s
        WHERE id=%(id)s
        """
        data['id'] = id
        result = self.execute_query(query, data)
        
        # Si le livre est rendu, le marquer comme disponible
        if result and data.get('statut') == 'rendu':
            # Récupérer l'ID du livre
            loan = self.find_by_id(id)
            if loan:
                update_book = "UPDATE livres SET disponible = TRUE WHERE id = %s"
                self.execute_query(update_book, (loan['livre_id'],))
        
        return result
    
    def find_with_details(self):
        """Récupérer les emprunts avec détails utilisateur et livre"""
        query = """
        SELECT e.*, 
               u.nom, u.prenom, 
               l.titre, l.auteur
        FROM emprunts e
        JOIN utilisateurs u ON e.utilisateur_id = u.id
        JOIN livres l ON e.livre_id = l.id
        ORDER BY e.date_emprunt DESC
        """
        return self.execute_query(query, fetch=True)
