class AuthState:
    def __init__(self):
        self.is_authenticated = False
        self.user = None

# Instancia global que se importará en otras partes de la aplicación
auth_state = AuthState()
