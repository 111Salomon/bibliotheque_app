import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.utilisateur_controller import UtilisateurController
from controller.livre_controller import LivreController
from controller.emprunt_controller import EmpruntController
from view.web_view import WebView

class MainController:
    def __init__(self):
        print("Initialisation des contrôleurs...")
        try:
            self.utilisateur_controller = UtilisateurController()
            self.livre_controller = LivreController()
            self.emprunt_controller = EmpruntController()
            print("Contrôleurs initialisés")
        except Exception as e:
            print(f"Erreur initialisation: {e}")
            raise

def main():
    print("Démarrage de l'application Bibliothèque MVC")
    print("=" * 50)
    
    try:
        # Test de connexion base de données
        from config.database import Database
        db = Database()
        connection = db.get_connection()
        if connection and connection.is_connected():
            print("Connexion MySQL OK")
            db.disconnect()
        else:
            print("Problème de connexion MySQL")
            return
        
        # Initialisation des contrôleurs
        main_controller = MainController()
        
        # Démarrage de l'interface web
        print("Démarrage du serveur web...")
        web_view = WebView(main_controller)
        web_view.start_server()
        
    except KeyboardInterrupt:
        print("\n Application arrêtée par l'utilisateur")
    except Exception as e:
        print(f"\n Erreur critique: {e}")
        print(" Vérifiez la configuration de la base de données")

if __name__ == "__main__":
    main()