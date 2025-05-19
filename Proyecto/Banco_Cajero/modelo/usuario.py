'''
Clase que representa el registro de un usuario
'''
class Usuario:
    def __init__(self, idusuario, idcliente, username, password, email, fecha_creacion, fecha_actualizacion):
        self.idusuario = idusuario 
        self.idcliente = idcliente 
        self.username = username
        self.password = password
        self.email = email
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion


    def __repr__(self):
        return f"<Usuario(id={self.idusuario}, id={self.idcliente}, username='{self.username}', password='{self.password}', email='{self.email}', fecha_creacion={self.fecha_creacion}, fecha_actualizacion={self.fecha_actualizacion})>"

