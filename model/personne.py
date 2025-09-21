# 3. MODEL/PERSONNE.PY (Classe mère)

class Personne:
    """Classe mère pour démontrer l'héritage"""
    def __init__(self, nom="", prenom="", email=""):
        self.nom = nom
        self.prenom = prenom
        self.email = email
    
    def get_nom_complet(self):
        return f"{self.prenom} {self.nom}"
    
    def valider_email(self):
        return "@" in self.email and "." in self.email
    
    def __str__(self):
        return self.get_nom_complet()