import time
import datetime

class Event:
    def _init_(self, builder):
        self.ID = builder.ID
        self.nombre = builder.nombre
        self.fecha: datetime = builder.fecha
        self.hora: time = builder.hora
        self.tipo = builder.tipo
        self.categoria = builder.categoria  # Añadido el campo categoría
        self.profesorID = builder.profesorID  # Añadido el ID del profesor
        self.podio = builder.podio  # Añadido el campo podio

class EventBuilder:
    def _init_(self):
        self.ID = None
        self.nombre = None
        self.fecha = None
        self.hora = None
        self.tipo = None
        self.categoria = None
        self.profesorID = None
        self.podio = None
    
    def set_ID(self, ID):
        self.ID = ID
        return self

    def set_nombre(self, nombre):
        self.nombre = nombre
        return self

    def set_fecha(self, fecha):
        self.fecha = fecha
        return self

    def set_hora(self, hora):
        self.hora = hora
        return self

    def set_tipo(self, tipo):
        self.tipo = tipo
        return self

    def set_categoria(self, categoria):
        self.categoria = categoria
        return self

    def set_profesorID(self, profesorID):
        self.profesorID = profesorID
        return self

    def set_podio(self, podio):
        self.podio = podio
        return self

    def build(self):
        return Event(self)