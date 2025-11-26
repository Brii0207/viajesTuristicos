from datetime import date
from Pago import Pago

class PagoTarjeta(Pago):
    """Implementación de Pago para tarjetas."""
    def __init__(self, id=0, monto=0.0, fecha=date.today(), numero="", vencimiento=date.today()):
        super().__init__(id, monto, fecha)
        self._numero = numero
        self._vencimiento = vencimiento

    def get_numero(self):
        return self._numero

    def set_numero(self, numero):
        self._numero = numero

    def get_vencimiento(self):
        return self._vencimiento

    def set_vencimiento(self, vencimiento):
        self._vencimiento = vencimiento

    def procesar(self):
        print(f"Procesando pago con tarjeta: {self._numero} por ${self.get_monto()}")
        return True