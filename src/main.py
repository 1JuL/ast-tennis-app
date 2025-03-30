import flet as ft
from pages.registration import Registration
from pages.login import Login
from pages.nav_buttons import nav_buttons

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
        content= ft.Row(
            [
                # Imagen a la izquierda
                ft.Container(
                    content=ft.Image(
                        src="./src/assets/ast-tennis-logo.png",
                        width=350,
                        height=350
                    ),
                    expand=True
                ),
                # Controles a la derecha
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "AST Tennis",
                                size=32,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.BLACK,
                                style=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                "¿Que vamos a hacer hoy?",
                                size=16,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.BLACK87
                            ),
                            ft.ElevatedButton(
                                text="Iniciar sesión",
                                height=50,
                                width=250,
                                color='#0F3BAC',
                                bgcolor='#FEF7FF',
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation=5
                                ),
                                on_click=lambda _: go_to_login(),
                            ),
                            ft.ElevatedButton(
                                text="Registrarse",
                                height=50,
                                width=250,
                                color='#0F3BAC',
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation=5
                                ),
                                bgcolor='#FEF7FF',
                                on_click=lambda _: go_to_registration()
                            ),
                            ft.ElevatedButton(
                                text="Salir",
                                height=50,
                                width=250,
                                color='#B3261E',
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation=5
                                ),
                                bgcolor = '#F9DEDC',
                                on_click=lambda _: page.window.close()
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
        gradient= ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_200], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
        expand=True
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
        page.bgcolor = ft.Colors.WHITE
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        # Asignamos el callback para volver al menú principal
        page.on_back = show_main_menu

        # Importamos la vista de registro desde pages/registration.py
        reg_view = Registration(page)
        page.controls = [reg_view]
        page.update()
    
    def go_to_nav_buttons():
        page.clean()
        page.bgcolor = ft.Colors.WHITE
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        # Asignamos el callback para volver al menú principal
        page.on_back = show_main_menu

        # Importamos la vista de registro desde pages/registration.py
        nav_view = nav_buttons(page, show_main_menu)
        page.controls = [nav_view]
        page.update()

    # Mostrar inicialmente el menú principal
    show_main_menu()

ft.app(target=main, assets_dir='assets')
