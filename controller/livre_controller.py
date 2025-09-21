# 
# CONTRÔLEUR LIVRE CORRIGÉ
# ====================

from controller.base_controller import BaseController
from model.livre import Livre

class LivreController(BaseController):
    def __init__(self):
        super().__init__(Livre())
    
    def get_livres_disponibles(self):
        """Récupérer les livres disponibles"""
        try:
            return self.model.find_disponibles()
        except Exception as e:
            print(f"Erreur récupération livres disponibles: {e}")
            return []
    
    def create(self, data):
        """Créer un livre avec validation"""
        try:
            # Validation des données
            if not data.get('titre', '').strip():
                print("Titre requis")
                return None
            
            if not data.get('auteur', '').strip():
                print("Auteur requis")
                return None
            
            # Nettoyer les données
            clean_data = {
                'titre': data.get('titre', '').strip(),
                'auteur': data.get('auteur', '').strip(),
                'isbn': data.get('isbn', '').strip(),
                'genre': data.get('genre', '').strip(),
                'annee_publication': int(data.get('annee_publication', 0)) if data.get('annee_publication') else None
            }
            
            result = super().create(clean_data)
            if result:
                print(f"Livre créé: {clean_data['titre']}")
            return result
            
        except Exception as e:
            print(f"Erreur création livre: {e}")
            return None
