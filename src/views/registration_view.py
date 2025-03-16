import flet as ft
from controllers.registration_controller import RegistrationController

class RegistrationView:
    def __init__(self, controller):
        self.controller = controller
        # Inicializamos el controlador específico para el registro
        self.reg_controller = RegistrationController(self)
        
        
        container = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    ft.Text(
                        "Registro",
                        size=30,
                        text_align="center",
                        weight="w900"
                    ),
                    padding=ft.padding.only(20, 20),
                    alignment=ft.alignment.center
                ),
                
                # Sección desplazable
                ft.Container(
                    content=ft.Column(
                        [
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text="Nombre",
                                border="underline",
                                color="black",
                                prefix_icon=ft.icons.PERSON
                            ),
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text="Apellidos",
                                border="underline",
                                color="black",
                                prefix_icon=ft.icons.PERSON
                            ),
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text="Fecha de nacimiento",
                                border="underline",
                                color="black",
                                prefix_icon=ft.icons.CALENDAR_MONTH
                            ),
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text="Teléfono",
                                border="underline",
                                color="black",
                                prefix_icon=ft.icons.PHONE
                            ),
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text="Dirección",
                                border="underline",
                                color="black",
                                prefix_icon=ft.icons.HOME
                            ),
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text="Correo electrónico",
                                border="underline",
                                color="black",
                                prefix_icon=ft.icons.EMAIL
                            ),
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text="Contraseña",
                                border="underline",
                                color="black",
                                password=True,
                                can_reveal_password=True,
                                prefix_icon=ft.icons.LOCK
                            ),
                        ],
                        spacing=10,
                        scroll=ft.ScrollMode.ALWAYS  # Permite hacer scroll si hay más contenido
                    ),
                    height=300,  # Limita el tamaño del área desplazable
                ),

                ft.Container(
                    ft.ElevatedButton(
                        text="Registrarse",
                        width=280,
                        bgcolor="black"
                    ),
                    padding=ft.padding.only(20, 10)
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="Volver",
                        width=280,
                        bgcolor="black",
                    ),
                    padding=ft.padding.only(20, 10)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        border_radius=20,
        width=320,
        height=500,
        gradient=ft.LinearGradient(
            [ft.colors.PURPLE, ft.colors.PINK, ft.colors.RED]
        ),
        padding=ft.padding.all(10)
    )
        # Definición de los campos de entrada
        
        # Botón para enviar el registro
        self.btn_register = ft.ElevatedButton(
            "Registrar",
            on_click=self.reg_controller.register
        )
        
        # Botón para volver al menú principal
        self.btn_back = ft.TextButton("Volver al Menú", on_click=self.on_back_click)
        
        self.view = container
        
    def on_back_click(self, e):
        self.controller.show_main_menu()
