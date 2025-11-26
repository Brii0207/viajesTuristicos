from Usuario import Usuario

class Administrador(Usuario):
    """Clase que representa a un Administrador. Hereda de Usuario."""
    
    def __init__(self, id=0, nombre="", email="", password="", tipo=2, departamento=""):
        super().__init__(id, nombre, email, password, tipo)
        self._departamento = departamento

    def get_departamento(self):
        return self._departamento

    def set_departamento(self, departamento):
        self._departamento = departamento

    def gestionar_vuelo(self, vuelo):
        print(f"Admin {self.get_nombre()} gestiona vuelo ID: {vuelo.get_id()}")

    def gestionar_hotel(self, hotel):
        print(f"Admin {self.get_nombre()} gestiona hotel: {hotel.get_nombre()}")