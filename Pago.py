from datetime import date

class Pago:
    """Clase abstracta base para los pagos."""
    def __init__(self, id=0, monto=0.0, fecha=date.today()):
        self._id = id
        self._monto = monto
        self._fecha = fecha

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_monto(self):
        return self._monto

    def set_monto(self, monto):
        self._monto = monto

    def get_fecha(self):
        return self._fecha

    def set_fecha(self, fecha):
        self._fecha = fecha

    def procesar(self):
        raise NotImplementedError("Este método debe ser implementado en una subclase.")