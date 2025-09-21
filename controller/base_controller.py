# 9. CONTROLLER/BASE_CONTROLLER.PY
# ====================
class BaseController:
    def __init__(self, model):
        self.model = model
    
    def get_all(self):
        try:
            return self.model.find_all()
        except Exception as e:
            print(f"Erreur lors de la récupération: {e}")
            return []
    
    def get_by_id(self, id):
        try:
            return self.model.find_by_id(id)
        except Exception as e:
            print(f"Erreur lors de la récupération par ID: {e}")
            return None
    
    def create(self, data):
        try:
            return self.model.create(data)
        except Exception as e:
            print(f"Erreur lors de la création: {e}")
            return None
    
    def update(self, id, data):
        try:
            return self.model.update(id, data)
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return None
    
    def delete(self, id):
        try:
            return self.model.delete(id)
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return None