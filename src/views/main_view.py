import flet as ft

class MainView:
    def __init__(self, controller):
        self.controller = controller

        self.view = ft.Container(
            content=ft.Row(
                [
                    # Imagen grande a la izquierda
                    ft.Container(
                        content=ft.Image(
                            src="https://picsum.photos/600",
                            width=600,
                            height=600
                        ),
                        expand=True
                    ),

                    # Controles de login/registro a la derecha
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Image(
                                    src="https://picsum.photos/200",
                                    width=200,
                                    height=200
                                ),
                                ft.Text(
                                    "Bienvenido a AST Tennis. Por favor seleccione una opción.",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.ElevatedButton(
                                    text="Iniciar sesión",
                                    width=250,
                                    on_click=self.on_login_click
                                ),
                                ft.ElevatedButton(
                                    text="Registrarse",
                                    width=250,
                                    on_click=self.on_registration_click
                                ),
                                ft.ElevatedButton(
                                    text="Salir",
                                    width=250,
                                    on_click=lambda _: self.on_exit_click
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            width=800,
            expand=True,
            gradient=ft.LinearGradient(
                colors=[ft.colors.BLUE_50, ft.colors.BLUE_200, ft.colors.BLUE_400],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            ),
        )

    def on_registration_click(self, e):
        self.controller.go_to_registration()

    def on_login_click(self, e):
        self.controller.go_to_login()
    
    def on_exit_click(self, e):
        self.controller.page.window_close()


    
