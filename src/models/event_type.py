class Event_Type:
    def __init__(self, builder):
        self.tipo = builder.tipo
        self.eventoID = builder.eventoID
        self.profesorID = builder.profesorID
        self.podio = builder.podio

class Event_TypeBuilder:
    def __init__(self):
        self.tipo = None
        self.eventoID = None
        self.profesorID = None
        self.podio = None
    
    def set_tipo(self, tipo):
        self.tipo = tipo
        return self
    
    def set_eventoID(self, eventoID):
        self.eventoID = eventoID
        return self
    
    def set_profesorID(self, profesorID):
        self.profesorID = profesorID
        return self
    
    def set_podio(self, podio):
        self.podio = podio
        return self
    
    def build(self):
        return Event_Type(self)