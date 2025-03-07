import flet as ft
from controllers.registration_controller import RegistrationController

class RegistrationView:
    def __init__(self, controller):
        self.controller = controller
        # Inicializamos el controlador específico para el registro
        self.reg_controller = RegistrationController(self)
        
        # Definición de los campos de entrada
        self.txt_username = ft.TextField(label="Nombre de Usuario")
        self.txt_email = ft.TextField(label="Correo Electrónico")
        self.txt_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
        
        # Botón para enviar el registro
        self.btn_register = ft.ElevatedButton(
            "Registrar",
            on_click=self.reg_controller.register
        )
        
        # Botón para volver al menú principal
        self.btn_back = ft.TextButton("Volver al Menú", on_click=self.on_back)
        
        self.view = ft.Column(
            [
                ft.Text("Registro", style="headlineMedium"),
                self.txt_username,
                self.txt_email,
                self.txt_password,
                self.btn_register,
                self.btn_back
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True
        )
        
    def on_back(self, e):
        self.controller.show_main_menu()
