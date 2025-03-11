import flet as ft
from controllers.registration_controller import RegistrationController

class RegistrationView:
    def __init__(self, controller):
        self.controller = controller
        # Inicializamos el controlador específico para el registro
        self.reg_controller = RegistrationController(self)
        
        
        container = ft.Container(
            ft.Column([
                ft.Container(
                    ft.Text(
                        "Registro",
                        width=320,
                        size=30,
                        text_align="center",
                        weight="w900"),
                    padding=ft.padding.only(20,20)
                ),
                ft.Container(
                    ft.TextField(
                       width=280,
                       height=40,
                       hint_text="Correo electrónico",
                       border="underline",
                       color="black",
                       prefix_icon=ft.icons.EMAIL
                    ),padding=ft.padding.only(20,20)
                ),
                ft.Container(
                    ft.TextField(
                       width=280,
                       height=40,
                       hint_text="Contraseña",
                       border="underline",
                       color="black",
                       password=True,
                       can_reveal_password=True,
                       prefix_icon=ft.icons.LOCK
                    ),padding=ft.padding.only(20,20)
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="Registrase",
                        width=280,
                        bgcolor="black"
                        
                    ),padding=ft.padding.only(20,20)
                    
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="Volver",
                        width=280,
                        bgcolor="black",
                        on_click=self.on_back
                        
                    ),padding=ft.padding.only(20,20)
                ),
                
            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            
            border_radius=20,
            width=320,
            height=500,
            gradient= ft.LinearGradient([ft.colors.PURPLE,
                ft.colors.PINK,
                ft.colors.RED
            ])
        )
        
        # Definición de los campos de entrada
        
        # Botón para enviar el registro
        self.btn_register = ft.ElevatedButton(
            "Registrar",
            on_click=self.reg_controller.register
        )
        
        # Botón para volver al menú principal
        self.btn_back = ft.TextButton("Volver al Menú", on_click=self.on_back)
        
        self.view = container
        
    def on_back(self, e):
        self.controller.show_main_menu()
