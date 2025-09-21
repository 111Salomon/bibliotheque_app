# VIEW/WEB_VIEW.PY 
# ====================

from view.base_view import BaseView
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
import cgi
from io import StringIO

class WebView(BaseView):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.port = 8000
    
    def start_server(self):
        handler = self.create_handler()
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"Serveur démarré sur http://localhost:{self.port}")
            print("Application Bibliothèque MVC")
            print("Appuyez sur Ctrl+C pour arrêter")
            httpd.serve_forever()
    
    def create_handler(self):
        view = self
        
        class RequestHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                return view.handle_get_request(self)
            
            def do_POST(self):
                return view.handle_post_request(self)
            
            def log_message(self, format, *args):
                # Supprime les logs HTTP pour plus de clarté
                pass
        
        return RequestHandler
    
    def handle_get_request(self, handler):
        """Gestion des requêtes GET"""
        url = urlparse(handler.path)
        path = url.path
        query_params = parse_qs(url.query)
        
        try:
            # Routes GET
            if path == "/" or path == "/index":
                content = self.render_homepage()
                
            elif path == "/utilisateurs":
                if 'action' in query_params and query_params['action'][0] == 'delete':
                    # Suppression d'utilisateur
                    user_id = int(query_params['id'][0])
                    success = self.controller.utilisateur_controller.delete(user_id)
                    # Redirection après suppression
                    handler.send_response(302)
                    handler.send_header('Location', '/utilisateurs?message=deleted')
                    handler.end_headers()
                    return
                else:
                    # Liste des utilisateurs
                    content = self.render_users_page()
                    
            elif path == "/livres":
                if 'action' in query_params and query_params['action'][0] == 'delete':
                    # Suppression de livre
                    book_id = int(query_params['id'][0])
                    success = self.controller.livre_controller.delete(book_id)
                    handler.send_response(302)
                    handler.send_header('Location', '/livres?message=deleted')
                    handler.end_headers()
                    return
                else:
                    content = self.render_books_page()
                    
            elif path == "/emprunts":
                if 'action' in query_params and query_params['action'][0] == 'return':
                    # Marquer comme rendu
                    loan_id = int(query_params['id'][0])
                    from datetime import date
                    update_data = {
                        'date_retour_effective': date.today().strftime('%Y-%m-%d'),
                        'statut': 'rendu'
                    }
                    success = self.controller.emprunt_controller.update(loan_id, update_data)
                    handler.send_response(302)
                    handler.send_header('Location', '/emprunts?message=returned')
                    handler.end_headers()
                    return
                else:
                    content = self.render_loans_page()
                    
            elif path.startswith("/static/"):
                # Fichiers statiques (CSS, JS, images)
                return super(type(handler), handler).do_GET()
                
            else:
                # Page non trouvée
                content = self.render_404_page()
                handler.send_response(404)
            
            # Envoyer la réponse HTML
            if 'content' in locals():
                handler.send_response(200)
                handler.send_header('Content-type', 'text/html; charset=utf-8')
                handler.end_headers()
                handler.wfile.write(content.encode('utf-8'))
            
        except Exception as e:
            print(f"Erreur GET: {e}")
            error_content = self.render_error_page(str(e))
            handler.send_response(500)
            handler.send_header('Content-type', 'text/html; charset=utf-8')
            handler.end_headers()
            handler.wfile.write(error_content.encode('utf-8'))
    
    def handle_post_request(self, handler):
        """Gestion des requêtes POST"""
        url = urlparse(handler.path)
        path = url.path
        
        try:
            # Lire les données POST
            content_length = int(handler.headers.get('Content-Length', 0))
            post_data = handler.rfile.read(content_length).decode('utf-8')
            
            # Parser les données du formulaire
            form_data = {}
            if post_data:
                pairs = post_data.split('&')
                for pair in pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        # Décoder les caractères URL
                        key = key.replace('+', ' ')
                        value = value.replace('+', ' ')
                        # Décoder les caractères spéciaux
                        import urllib.parse
                        key = urllib.parse.unquote(key)
                        value = urllib.parse.unquote(value)
                        form_data[key] = value
            
            print(f"POST {path}: {form_data}")
            
            success = False
            redirect_url = "/"
            
            # Routes POST
            if path == "/utilisateurs/create":
                # Créer utilisateur
                success = self.controller.utilisateur_controller.create_utilisateur(
                    form_data.get('nom', ''),
                    form_data.get('prenom', ''),
                    form_data.get('email', ''),
                    form_data.get('telephone', '')
                )
                redirect_url = "/utilisateurs?message=created" if success else "/utilisateurs?error=create_failed"
                
            elif path == "/utilisateurs/update":
                # Modifier utilisateur
                user_id = int(form_data.get('id', 0))
                update_data = {
                    'nom': form_data.get('nom', ''),
                    'prenom': form_data.get('prenom', ''),
                    'email': form_data.get('email', ''),
                    'telephone': form_data.get('telephone', '')
                }
                success = self.controller.utilisateur_controller.update(user_id, update_data)
                redirect_url = "/utilisateurs?message=updated" if success else "/utilisateurs?error=update_failed"
                
            elif path == "/livres/create":
                # Créer livre
                success = self.controller.livre_controller.create({
                    'titre': form_data.get('titre', ''),
                    'auteur': form_data.get('auteur', ''),
                    'isbn': form_data.get('isbn', ''),
                    'genre': form_data.get('genre', ''),
                    'annee_publication': int(form_data.get('annee_publication', 0))
                })
                redirect_url = "/livres?message=created" if success else "/livres?error=create_failed"
                
            elif path == "/livres/update":
                # Modifier livre
                book_id = int(form_data.get('id', 0))
                update_data = {
                    'titre': form_data.get('titre', ''),
                    'auteur': form_data.get('auteur', ''),
                    'isbn': form_data.get('isbn', ''),
                    'genre': form_data.get('genre', ''),
                    'annee_publication': int(form_data.get('annee_publication', 0))
                }
                success = self.controller.livre_controller.update(book_id, update_data)
                redirect_url = "/livres?message=updated" if success else "/livres?error=update_failed"
                
            elif path == "/emprunts/create":
                # Créer emprunt
                from datetime import date, timedelta
                date_retour = (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
                
                success = self.controller.emprunt_controller.create({
                    'utilisateur_id': int(form_data.get('utilisateur_id', 0)),
                    'livre_id': int(form_data.get('livre_id', 0)),
                    'date_retour_prevue': date_retour
                })
                redirect_url = "/emprunts?message=created" if success else "/emprunts?error=create_failed"
                
            # Redirection après traitement
            handler.send_response(302)
            handler.send_header('Location', redirect_url)
            handler.end_headers()
            
            if success:
                print("Opération réussie")
            else:
                print("Échec de l'opération")
            
        except Exception as e:
            print(f"Erreur POST: {e}")
            handler.send_response(302)
            handler.send_header('Location', '/?error=server_error')
            handler.end_headers()
    
    def render_homepage(self):
        """Page d'accueil"""
        # Statistiques
        try:
            total_users = len(self.controller.utilisateur_controller.get_all())
            total_books = len(self.controller.livre_controller.get_all())
            total_loans = len(self.controller.emprunt_controller.get_all())
        except:
            total_users = total_books = total_loans = 0
        
        return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Accueil - Bibliothèque MVC</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            {self.render_navbar()}
            
            <div class="container mt-5">
                <div class="row">
                    <div class="col-12 text-center mb-5">
                        <h1 class="display-4 mb-4">
                            <i class="fas fa-book-open text-primary me-3"></i>
                            Bibliothèque MVC
                        </h1>
                        <p class="lead">Application de démonstration - Architecture MVC en Python pur</p>
                    </div>
                </div>

                <!-- Statistiques -->
                <div class="row mb-5">
                    <div class="col-md-4">
                        <div class="card text-center border-primary">
                            <div class="card-body">
                                <i class="fas fa-users text-primary fa-3x mb-3"></i>
                                <h3>{total_users}</h3>
                                <p>Utilisateurs</p>
                                <a href="/utilisateurs" class="btn btn-primary">Gérer</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card text-center border-success">
                            <div class="card-body">
                                <i class="fas fa-book text-success fa-3x mb-3"></i>
                                <h3>{total_books}</h3>
                                <p>Livres</p>
                                <a href="/livres" class="btn btn-success">Gérer</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card text-center border-warning">
                            <div class="card-body">
                                <i class="fas fa-exchange-alt text-warning fa-3x mb-3"></i>
                                <h3>{total_loans}</h3>
                                <p>Emprunts</p>
                                <a href="/emprunts" class="btn btn-warning">Gérer</a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="alert alert-info">
                    <h5><i class="fas fa-info-circle me-2"></i>Python pur</h5>
                    <p class="mb-0">Application web de gestion de bibliothèque développée en Python pur suivant l'architecture MVC (Model-View-Controller)</p>
                </div>
            </div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """
    
    def render_users_page(self):
        """Page de gestion des utilisateurs"""
        users = self.controller.utilisateur_controller.get_all() or []
        
        # Messages de feedback
        message_html = ""
        import urllib.parse
        url_parts = urllib.parse.urlparse(self.controller.__dict__.get('current_url', ''))
        query_params = urllib.parse.parse_qs(url_parts.query)
        
        if 'message' in query_params:
            message = query_params['message'][0]
            if message == 'created':
                message_html = '<div class="alert alert-success">Utilisateur créé avec succès!</div>'
            elif message == 'updated':
                message_html = '<div class="alert alert-success">Utilisateur modifié avec succès!</div>'
            elif message == 'deleted':
                message_html = '<div class="alert alert-success">Utilisateur supprimé avec succès!</div>'
        
        users_html = ""
        for user in users:
            users_html += f"""
            <tr>
                <td>{user.get('id', '')}</td>
                <td><strong>{user.get('prenom', '')} {user.get('nom', '')}</strong></td>
                <td>{user.get('email', '')}</td>
                <td>{user.get('telephone', '')}</td>
                <td>{user.get('date_inscription', '')}</td>
                <td><span class="badge bg-success">Actif</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editUser({user.get('id', '')}, '{user.get('nom', '')}', '{user.get('prenom', '')}', '{user.get('email', '')}', '{user.get('telephone', '')}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteUser({user.get('id', '')}, '{user.get('prenom', '')} {user.get('nom', '')}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Utilisateurs - Bibliothèque MVC</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            {self.render_navbar()}

            <div class="container mt-4">
                {message_html}
                
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2><i class="fas fa-users text-primary me-2"></i>Gestion des Utilisateurs</h2>
                    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#userModal" onclick="resetForm()">
                        <i class="fas fa-plus me-2"></i>Nouvel utilisateur
                    </button>
                </div>

                <div class="card">
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Nom Complet</th>
                                        <th>Email</th>
                                        <th>Téléphone</th>
                                        <th>Date Inscription</th>
                                        <th>Statut</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {users_html}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Modal Formulaire -->
                <div class="modal fade" id="userModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="modalTitle">
                                    <i class="fas fa-user-plus me-2"></i>Nouvel Utilisateur
                                </h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <form id="userForm" method="POST" action="/utilisateurs/create">
                                <div class="modal-body">
                                    <input type="hidden" id="userId" name="id" value="">
                                    <div class="mb-3">
                                        <label for="nom" class="form-label">Nom *</label>
                                        <input type="text" class="form-control" id="nom" name="nom" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="prenom" class="form-label">Prénom *</label>
                                        <input type="text" class="form-control" id="prenom" name="prenom" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="email" class="form-label">Email *</label>
                                        <input type="email" class="form-control" id="email" name="email" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="telephone" class="form-label">Téléphone</label>
                                        <input type="tel" class="form-control" id="telephone" name="telephone">
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                                    <button type="submit" class="btn btn-primary">
                                        <i class="fas fa-save me-2"></i>Enregistrer
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
            <script>
                function resetForm() {{
                    document.getElementById('userForm').action = '/utilisateurs/create';
                    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-user-plus me-2"></i>Nouvel Utilisateur';
                    document.getElementById('userId').value = '';
                    document.getElementById('nom').value = '';
                    document.getElementById('prenom').value = '';
                    document.getElementById('email').value = '';
                    document.getElementById('telephone').value = '';
                }}

                function editUser(id, nom, prenom, email, telephone) {{
                    document.getElementById('userForm').action = '/utilisateurs/update';
                    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-user-edit me-2"></i>Modifier Utilisateur';
                    document.getElementById('userId').value = id;
                    document.getElementById('nom').value = nom;
                    document.getElementById('prenom').value = prenom;
                    document.getElementById('email').value = email;
                    document.getElementById('telephone').value = telephone;
                    
                    new bootstrap.Modal(document.getElementById('userModal')).show();
                }}

                function deleteUser(id, name) {{
                    if (confirm('Êtes-vous sûr de vouloir supprimer ' + name + ' ?')) {{
                        window.location.href = '/utilisateurs?action=delete&id=' + id;
                    }}
                }}
            </script>
        </body>
        </html>
        """
    
    def render_books_page(self):
        """Page de gestion des livres"""
        books = self.controller.livre_controller.get_all() or []
        
        books_html = ""
        for book in books:
            disponible = "Disponible" if book.get('disponible', True) else "Emprunté"
            badge_class = "bg-success" if book.get('disponible', True) else "bg-warning"

            # Pré-calculer les valeurs échappées pour éviter les backslashes dans les expressions f-string
            titre_raw = book.get('titre', '') or ''
            # Échapper uniquement les apostrophes pour l'injection dans les attributs JS entre quotes simples
            titre_escaped = titre_raw.replace("'", "\\'")
            auteur = book.get('auteur', '') or ''
            isbn = book.get('isbn', '') or ''
            genre = book.get('genre', '') or ''
            annee = book.get('annee_publication', 0) or 0

            books_html += f"""
            <tr>
                <td>{book.get('id', '')}</td>
                <td><strong>{titre_raw}</strong></td>
                <td>{auteur}</td>
                <td>{genre}</td>
                <td>{book.get('annee_publication', '')}</td>
                <td>{isbn}</td>
                <td><span class="badge {badge_class}">{disponible}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editBook({book.get('id', '')}, '{titre_escaped}', '{auteur}', '{isbn}', '{genre}', {annee})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteBook({book.get('id', '')}, '{titre_escaped}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Livres - Bibliothèque MVC</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            {self.render_navbar()}

            <div class="container mt-4">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2><i class="fas fa-book text-success me-2"></i>Catalogue des Livres</h2>
                    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#bookModal" onclick="resetBookForm()">
                        <i class="fas fa-plus me-2"></i>Nouveau livre
                    </button>
                </div>

                <div class="card">
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Titre</th>
                                        <th>Auteur</th>
                                        <th>Genre</th>
                                        <th>Année</th>
                                        <th>ISBN</th>
                                        <th>Statut</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {books_html}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Modal Livre -->
                <div class="modal fade" id="bookModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="bookModalTitle">
                                    <i class="fas fa-book-plus me-2"></i>Nouveau Livre
                                </h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <form id="bookForm" method="POST" action="/livres/create">
                                <div class="modal-body">
                                    <input type="hidden" id="bookId" name="id" value="">
                                    <div class="mb-3">
                                        <label for="titre" class="form-label">Titre *</label>
                                        <input type="text" class="form-control" id="titre" name="titre" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="auteur" class="form-label">Auteur *</label>
                                        <input type="text" class="form-control" id="auteur" name="auteur" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="isbn" class="form-label">ISBN</label>
                                        <input type="text" class="form-control" id="isbn" name="isbn">
                                    </div>
                                    <div class="mb-3">
                                        <label for="genre" class="form-label">Genre</label>
                                        <input type="text" class="form-control" id="genre" name="genre">
                                    </div>
                                    <div class="mb-3">
                                        <label for="annee_publication" class="form-label">Année de publication</label>
                                        <input type="number" class="form-control" id="annee_publication" name="annee_publication" min="1000" max="2030">
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                                    <button type="submit" class="btn btn-success">
                                        <i class="fas fa-save me-2"></i>Enregistrer
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
            <script>
                function resetBookForm() {{
                    document.getElementById('bookForm').action = '/livres/create';
                    document.getElementById('bookModalTitle').innerHTML = '<i class="fas fa-book-plus me-2"></i>Nouveau Livre';
                    document.getElementById('bookId').value = '';
                    document.getElementById('titre').value = '';
                    document.getElementById('auteur').value = '';
                    document.getElementById('isbn').value = '';
                    document.getElementById('genre').value = '';
                    document.getElementById('annee_publication').value = '';
                }}

                function editBook(id, titre, auteur, isbn, genre, annee) {{
                    document.getElementById('bookForm').action = '/livres/update';
                    document.getElementById('bookModalTitle').innerHTML = '<i class="fas fa-book-edit me-2"></i>Modifier Livre';
                    document.getElementById('bookId').value = id;
                    document.getElementById('titre').value = titre;
                    document.getElementById('auteur').value = auteur;
                    document.getElementById('isbn').value = isbn;
                    document.getElementById('genre').value = genre;
                    document.getElementById('annee_publication').value = annee;
                    
                    new bootstrap.Modal(document.getElementById('bookModal')).show();
                }}

                function deleteBook(id, titre) {{
                    if (confirm('Êtes-vous sûr de vouloir supprimer "' + titre + '" ?')) {{
                        window.location.href = '/livres?action=delete&id=' + id;
                    }}
                }}
            </script>
        </body>
        </html>
        """
    
    def render_loans_page(self):
        """Page de gestion des emprunts"""
        loans = self.controller.emprunt_controller.get_all_with_details() or []
        users = self.controller.utilisateur_controller.get_all() or []
        books = self.controller.livre_controller.get_livres_disponibles() or []
        
        loans_html = ""
        for loan in loans:
            status_class = "bg-warning" if loan.get('statut') == 'en_cours' else "bg-success"
            status_text = "En cours" if loan.get('statut') == 'en_cours' else "Rendu"
            
            loans_html += f"""
            <tr>
                <td>{loan.get('id', '')}</td>
                <td><strong>{loan.get('prenom', '')} {loan.get('nom', '')}</strong></td>
                <td>{loan.get('titre', '')}</td>
                <td>{loan.get('date_emprunt', '')}</td>
                <td>{loan.get('date_retour_prevue', '')}</td>
                <td>{loan.get('date_retour_effective', '') or '-'}</td>
                <td><span class="badge {status_class}">{status_text}</span></td>
                <td>
                    {'<button class="btn btn-sm btn-outline-success me-1" onclick="returnBook(' + str(loan.get('id', '')) + ')" title="Marquer comme rendu"><i class="fas fa-check"></i></button>' if loan.get('statut') == 'en_cours' else ''}
                </td>
            </tr>
            """
        
        # Options pour les utilisateurs
        users_options = ""
        for user in users:
            users_options += f'<option value="{user.get("id", "")}">{user.get("prenom", "")} {user.get("nom", "")}</option>'
        
        # Options pour les livres disponibles
        books_options = ""
        for book in books:
            books_options += f'<option value="{book.get("id", "")}">{book.get("titre", "")} - {book.get("auteur", "")}</option>'
        
        return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Emprunts - Bibliothèque MVC</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            {self.render_navbar()}

            <div class="container mt-4">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2><i class="fas fa-exchange-alt text-warning me-2"></i>Gestion des Emprunts</h2>
                    <button class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#loanModal">
                        <i class="fas fa-plus me-2"></i>Nouvel emprunt
                    </button>
                </div>

                <div class="card">
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Utilisateur</th>
                                        <th>Livre</th>
                                        <th>Date Emprunt</th>
                                        <th>Retour Prévu</th>
                                        <th>Retour Effectif</th>
                                        <th>Statut</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {loans_html}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Modal Emprunt -->
                <div class="modal fade" id="loanModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">
                                    <i class="fas fa-plus me-2"></i>Nouvel Emprunt
                                </h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <form method="POST" action="/emprunts/create">
                                <div class="modal-body">
                                    <div class="mb-3">
                                        <label for="utilisateur_id" class="form-label">Utilisateur *</label>
                                        <select class="form-control" id="utilisateur_id" name="utilisateur_id" required>
                                            <option value="">Choisir un utilisateur</option>
                                            {users_options}
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="livre_id" class="form-label">Livre disponible *</label>
                                        <select class="form-control" id="livre_id" name="livre_id" required>
                                            <option value="">Choisir un livre</option>
                                            {books_options}
                                        </select>
                                    </div>
                                    <div class="alert alert-info">
                                        <small>La date de retour sera automatiquement fixée à 30 jours à partir d'aujourd'hui.</small>
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                                    <button type="submit" class="btn btn-warning">
                                        <i class="fas fa-save me-2"></i>Créer l'emprunt
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
            <script>
                function returnBook(loanId) {{
                    if (confirm('Marquer ce livre comme rendu ?')) {{
                        window.location.href = '/emprunts?action=return&id=' + loanId;
                    }}
                }}
            </script>
        </body>
        </html>
        """
    
    def render_navbar(self):
        """Barre de navigation commune"""
        return """
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/"><i class="fas fa-book-open me-2"></i>Bibliothèque MVC</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/"><i class="fas fa-home me-1"></i>Accueil</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/utilisateurs"><i class="fas fa-users me-1"></i>Utilisateurs</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/livres"><i class="fas fa-book me-1"></i>Livres</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/emprunts"><i class="fas fa-exchange-alt me-1"></i>Emprunts</a>
                        </li>
                    </ul>
                    <span class="navbar-text">
                        <small> Salomon 2993 </small>
                    </span>
                </div>
            </div>
        </nav>
        """
    
    def render_404_page(self):
        """Page d'erreur 404"""
        return """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Page non trouvée</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5 text-center">
                <h1>404 - Page non trouvée</h1>
                <p><a href="/" class="btn btn-primary">Retour à l'accueil</a></p>
            </div>
        </body>
        </html>
        """
    
    def render_error_page(self, error_message):
        """Page d'erreur générale"""
        return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Erreur</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <div class="alert alert-danger">
                    <h4>Erreur</h4>
                    <p>{error_message}</p>
                    <a href="/" class="btn btn-primary">Retour à l'accueil</a>
                </div>
            </div>
        </body>
        </html>
        """
