from datetime import date

class Vuelo:
    """Representa un vuelo disponible para reserva."""
    
    def __init__(self, id=0, origen="", destino="", fecha=date.today(), precio=0.0):
        self._id = id
        self._origen = origen
        self._destino = destino
        self._fecha = fecha
        self._precio = precio

    def get_id(self):
        return self._id
    
    def set_id(self, id):
        self._id = id

    def get_origen(self):
        return self._origen

    def set_origen(self, origen):
        self._origen = origen

    def get_destino(self):
        return self._destino

    def set_destino(self, destino):
        self._destino = destino

    def get_fecha(self):
        return self._fecha

    def set_fecha(self, fecha):
        self._fecha = fecha

    def get_precio(self):
        return self._precio

    def set_precio(self, precio):
        self._precio = precio