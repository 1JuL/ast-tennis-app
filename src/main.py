import flet as ft
from pages.registration import Registration
from pages.login import Login

def main(page: ft.Page):
    page.title = "AST Tennis"
    page.bgcolor = ft.Colors.WHITE
    page.padding = 0
    page.horizontal_alignment = "stretch"
    page.vertical_alignment = "stretch"

    def show_main_menu():
        page.clean()
        page.bgcolor = ft.Colors.WHITE
        page.vertical_alignment = "stretch"
        page.horizontal_alignment = "stretch"
        # Permite que desde otras vistas se pueda volver al menú principal
        page.on_back = show_main_menu

        main_menu = ft.Container(
            content=ft.Row(
                [
                    # Imagen a la izquierda
                    ft.Container(
                        content=ft.Image(
                            src="src/assets/ast-tennis-logo.png",
                            width=600,
                            height=600
                        ),
                        expand=True
                    ),
                    # Controles a la derecha
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Bienvenido a AST Tennis. Por favor seleccione una opción.",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                    color=ft.Colors.BLACK
                                ),
                                ft.ElevatedButton(
                                    text="Iniciar sesión",
                                    width=250,
                                    on_click=lambda e: go_to_login()
                                ),
                                ft.ElevatedButton(
                                    text="Registrarse",
                                    width=250,
                                    on_click=lambda e: go_to_registration()
                                ),
                                ft.ElevatedButton(
                                    text="Salir",
                                    width=250,
                                    on_click=lambda e: page.destroy()
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
                colors=[ft.Colors.BLUE_50, ft.Colors.BLUE_200, ft.Colors.BLUE_400],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            ),
        )
        page.controls = [main_menu]
        page.update()

    def go_to_login():
        page.clean()
        page.bgcolor = ft.Colors.BLACK
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        # Asignamos el callback para volver al menú principal
        page.on_back = show_main_menu

        # Importamos la vista de registro desde pages/login.py
        login_view = Login(page)
        page.controls = [login_view]
        page.update()

    def go_to_registration():
        page.clean()
        page.bgcolor = ft.Colors.BLACK
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        # Asignamos el callback para volver al menú principal
        page.on_back = show_main_menu

        # Importamos la vista de registro desde pages/registration.py
        reg_view = Registration(page)
        page.controls = [reg_view]
        page.update()

    # Mostrar inicialmente el menú principal
    show_main_menu()

ft.app(target=main)
