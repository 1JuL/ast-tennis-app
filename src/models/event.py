import time, datetime

class Event:
    def __init__(self, builder):
        self.ID = builder.ID
        self.nombre = builder.nombre
        self.fecha: datetime = builder.fecha
        self.hora: time = builder.hora
        self.tipo = builder.tipo

class EventBuilder:
    def __init__(self):
        self.ID = None
        self.nombre = None
        self.fecha = None
        self.hora = None
        self.tipo = None
    
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

    def build(self):
        return Event(self)