from datetime import date

class Reserva:
    """Representa la unión de un cliente, un vuelo y un hotel."""
    
    def __init__(self, id=0, fecha=date.today(), estado="Pendiente", cliente=None, vuelo=None, hotel=None, total=0.0):
        self._id = id
        self._fecha = fecha
        self._estado = estado
        self._cliente = cliente 
        self._vuelo = vuelo     
        self._hotel = hotel   
        self._total = total     

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_fecha(self):
        return self._fecha

    def set_fecha(self, fecha):
        self._fecha = fecha

    def get_estado(self):
        return self._estado

    def set_estado(self, estado):
        self._estado = estado

    def get_cliente(self):
        return self._cliente

    def set_cliente(self, cliente):
        self._cliente = cliente

    def get_vuelo(self):
        return self._vuelo

    def set_vuelo(self, vuelo):
        self._vuelo = vuelo

    def get_hotel(self):
        return self._hotel

    def set_hotel(self, hotel):
        self._hotel = hotel

    def get_total(self):
        return self._total
    
    def set_total(self, total):
        self._total = total

    def calcular_total(self):
        """Calcula el total sumando los precios del vuelo y el hotel (solo si están disponibles)."""
        total = 0
        if self._vuelo is not None:
            total += self._vuelo.get_precio()
        if self._hotel is not None:
            total += self._hotel.get_precio_noche()
        self._total = total
        return total