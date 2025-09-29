# 7. VIEW/BASE_VIEW.PY

import os

class BaseView:
    def __init__(self):
        self.templates_dir = "templates"
    
    def render_template(self, template_name, context=None):
        template_path = os.path.join(self.templates_dir, template_name)
        
        if not os.path.exists(template_path):
            return f"<h1>Template non trouvé: {template_name}</h1>"
        
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remplacements simples des variables
        if context:
            for key, value in context.items():
                placeholder = f"{{{{{key}}}}}"
                if isinstance(value, list):
                    # Pour les listes, on génère du HTML
                    html_items = ""
                    for item in value:
                        if isinstance(item, dict):
                            html_items += self._dict_to_html_row(item)
                    content = content.replace(placeholder, html_items)
                else:
                    content = content.replace(placeholder, str(value))
        
        return content
    
    def _dict_to_html_row(self, item):
        # Convertit un dictionnaire en ligne de tableau HTML
        cells = ""
        for key, value in item.items():
            if key != 'id':  # On évite d'afficher l'ID
                cells += f"<td>{value}</td>"
        return f"<tr>{cells}</tr>"