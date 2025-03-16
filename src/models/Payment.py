import datetime


class Payment:
    
    def __init__(self, id, personaId, monto, fecha, estado = "Pendiente"):
        self.ID = id
        self.personaId = personaId
        self.monto = monto
        self.fecha: datetime = fecha
        self.estado = estado
        