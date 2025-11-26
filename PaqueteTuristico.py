from Vuelo import Vuelo
from Hotel import Hotel

class PaqueteTuristico:
    """Representa un paquete turístico predefinido."""
    
    def __init__(self, id=0, nombre="", descripcion="", vuelo=None, hotel=None, precio_total=0.0):
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion
        self._vuelo = vuelo
        self._hotel = hotel
        self._precio_total = precio_total

    def get_id(self):
        return self._id
    
    def set_vuelo(self, vuelo: Vuelo):
        self._vuelo = vuelo

    def set_hotel(self, hotel: Hotel):
        self._hotel = hotel

    def calcular_precio_total(self):
        total = 0
        if self._vuelo is not None:
            total += self._vuelo.get_precio()
        if self._hotel is not None:
            total += self._hotel.get_precio_noche()

        self._precio_total = total
        return total