from Usuario import Usuario

class Cliente(Usuario):
    """Clase que representa a un Cliente. Hereda de Usuario."""
    
    def __init__(self, id=0, nombre="", email="", password="", tipo=1, telefono="", historial=None):
        super().__init__(id, nombre, email, password, tipo) 
        self._telefono = telefono
        self._historial = historial if historial is not None else []

    def get_telefono(self):
        return self._telefono

    def set_telefono(self, telefono):
        self._telefono = telefono

    def get_historial(self):
        return self._historial

    def add_reserva(self, reserva):
        self._historial.append(reserva)
        