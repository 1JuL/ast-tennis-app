import flet as ft

class LoginView:
    def __init__(self, controller):
        self.controller = controller
        
        container = ft.Container(
            ft.Column([
                ft.Container(
                    ft.Text(
                        "Iniciar sesión",
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
                        text="Iniciar sesión",
                        width=280,
                        bgcolor="black"
                        
                    ),padding=ft.padding.only(20,20)
                    
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="Volver",
                        width=280,
                        bgcolor="black",
                        on_click=self.on_registration_click
                        
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
        
        # Botón para navegar a la pantalla de registro
        self.btn_registration = ft.ElevatedButton(
            "Ir a Registro",
            on_click=self.on_registration_click
        )
        
        self.view = container
        
    def on_registration_click(self, e):
        self.controller.go_to_registration()

    def on_back_click(self, e):
        self.controller.go_to_main_menu()
