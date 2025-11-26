class Hotel:
    """Representa un hotel disponible para reserva."""
    
    def __init__(self, id=0, nombre="", ubicacion="", precio_noche=0.0):
        self._id = id
        self._nombre = nombre
        self._ubicacion = ubicacion
        self._precio_noche = precio_noche

    def get_id(self):
        return self._id
    
    def set_id(self, id):
        self._id = id

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_ubicacion(self):
        return self._ubicacion

    def set_ubicacion(self, ubicacion):
        self._ubicacion = ubicacion

    def get_precio_noche(self):
        return self._precio_noche

    def set_precio_noche(self, precio_noche):
        self._precio_noche = precio_noche