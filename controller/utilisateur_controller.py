# CONTRÔLEUR UTILISATEUR CORRIGÉ

from controller.base_controller import BaseController
from model.utilisateur import Utilisateur

class UtilisateurController(BaseController):
    def __init__(self):
        super().__init__(Utilisateur())
    
    def create_utilisateur(self, nom, prenom, email, telephone=""):
        """Créer un utilisateur avec validation"""
        # Validation avec héritage de Personne
        from model.personne import Personne
        personne = Personne(nom, prenom, email)
        
        if not personne.valider_email():
            print("Email invalide")
            return None
        
        # Vérifier l'unicité de l'email
        existing_user = self.model.find_by_email(email)
        if existing_user:
            print("Email déjà utilisé")
            return None
        
        data = {
            'nom': nom.strip(),
            'prenom': prenom.strip(),
            'email': email.strip().lower(),
            'telephone': telephone.strip()
        }
        
        try:
            result = self.create(data)
            if result:
                print(f"Utilisateur créé: {personne.get_nom_complet()}")
            return result
        except Exception as e:
            print(f"Erreur création utilisateur: {e}")
            return None
