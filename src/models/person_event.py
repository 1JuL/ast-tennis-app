class Person_Event:
    def __init__(self, builder):
        self.personaID = builder.personaID
        self.eventoID = builder.eventoID
        self.asistencia = builder.asistencia

class Person_EventBuilder:
    def __init__(self):
        self.personaID = None
        self.eventoID = None
        self.asistencia = None
    
    def set_personaID(self, personaID):
        self.personaID = personaID
        return self
    
    def set_eventoID(self, eventoID):
        self.eventoID = eventoID
        return self
    
    def set_asistencia(self, asistencia):
        self.asistencia = asistencia
        return self
    
    def build(self):
        return Person_Event(self)