import datetime

class Person:
    def __init__(self, builder):
        self.nombre = builder.nombre
        self.apellido = builder.apellido
        self.fecha_nacimiento = builder.fecha_nacimiento
        self.telefono = builder.telefono
        self.direccion = builder.direccion
        self.email = builder.email
        self.categoria = builder.categoria
        self.estado = builder.estado
        self.rol = builder.rol


class PersonBuilder:
    def __init__(self):
        self.nombre = None
        self.apellido = None
        self.fecha_nacimiento = None
        self.telefono = None
        self.direccion = None
        self.email = None
        self.categoria = None
        self.estado = None
        self.rol = None
    
    def set_nombre(self, nombre):
        self.nombre = nombre
        return self
    
    def set_apellido(self, apellido):
        self.apellido = apellido
        return self
    
    def set_fecha_nacimiento(self, fecha_nacimiento):
        self.fecha_nacimiento = fecha_nacimiento
        return self
    
    def set_telefono(self, telefono):
        self.telefono = telefono
        return self
    
    def set_direccion(self, direccion):
        self.direccion = direccion
        return self
    
    def set_email(self, email):
        self.email = email
        return self
    
    def set_categoria(self, categoria):
        self.categoria = categoria
        return self
    
    def set_estado(self, estado):
        self.estado = estado
        return self
    
    def set_rol(self, rol):
        self.rol = rol
        return self
    
    def build(self):
        return Person(self)