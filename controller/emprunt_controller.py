from controller.base_controller import BaseController
from model.emprunt import Emprunt

class EmpruntController(BaseController):
    def __init__(self):
        super().__init__(Emprunt())
    
    def get_all_with_details(self):
        """Récupérer tous les emprunts avec détails"""
        try:
            return self.model.find_with_details()
        except Exception as e:
            print(f"Erreur récupération emprunts: {e}")
            return []
    
    def create(self, data):
        """Créer un emprunt avec validations"""
        try:
            # Vérifier que l'utilisateur existe
            from model.utilisateur import Utilisateur
            user_model = Utilisateur()
            user = user_model.find_by_id(data.get('utilisateur_id'))
            if not user:
                print("Utilisateur introuvable")
                return None
            
            # Vérifier que le livre existe et est disponible
            from model.livre import Livre
            book_model = Livre()
            book = book_model.find_by_id(data.get('livre_id'))
            if not book:
                print("Livre introuvable")
                return None
            
            if not book.get('disponible', False):
                print("Livre non disponible")
                return None
            
            result = super().create(data)
            if result:
                print(f"Emprunt créé: {book['titre']} pour {user['prenom']} {user['nom']}")
            return result
            
        except Exception as e:
            print(f"Erreur création emprunt: {e}")
            return None