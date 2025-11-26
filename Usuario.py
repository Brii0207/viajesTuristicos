class Usuario:
    """Clase base para todos los usuarios del sistema."""
    
    def __init__(self, id=0, nombre="", email="", password="", tipo=1): 
        self._id = id
        self._nombre = nombre
        self._email = email
        self._password = password
        self._tipo = tipo 

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def get_tipo(self):
        return self._tipo

    def set_tipo(self, tipo):
        self._tipo = tipo

    def logout(self):
        print(f"Sesión del usuario {self._nombre} cerrada.")