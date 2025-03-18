import flet as ft
from pages.gestionar_pagos import Gestionar_pagos
from pages.gestionar_torneos import Gestionar_torneos
from pages.gestionar_entrenamientos import Gestionar_entrenamientos  # Importa la nueva vista de entrenamientos
from pages.visualizar_entrenamientos import Visualizar_entrenamientos  # Importa la nueva vista de entrenamientos
def nav_buttons(page: ft.Page, show_main_menu):
    """
    Retorna un contenedor con botones de navegación para cargar otras vistas.
    El parámetro show_main_menu es la función que debe invocarse para volver al menú principal.
    """
    def go_back(e):
        # Llama directamente a la función del main para volver al menú principal
        show_main_menu()

    def show_nav_buttons():
        # Muestra nuevamente la vista de navegación
        page.clean()
        page.controls = [nav]
        page.update()

    def go_to_view(view_func):
        page.clean()
        page.bgcolor = ft.Colors.BLACK
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        # Para las vistas a las que se navega, asignamos que su "back" retorne a la vista de navegación
        page.on_back = show_nav_buttons
        nav_view = view_func(page)
        page.controls = [nav_view]
        page.update()

    nav = ft.Container(
        content=ft.Column(
            [
                ft.ElevatedButton(
                    text="Gestionar Pagos",
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: go_to_view(Gestionar_pagos)
                ),
                ft.ElevatedButton(
                    text="Gestionar Torneos",
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: go_to_view(Gestionar_torneos)
                ),
                ft.ElevatedButton(
                    text="Gestionar Entrenamientos",  # Botón para la nueva vista
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: go_to_view(Gestionar_entrenamientos)  # Llama a la vista de entrenamientos
                ),
                ft.ElevatedButton(
                    text="Visualizar Entrenamientos",  # Botón para la nueva vista
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: go_to_view(Visualizar_entrenamientos)  # Llama a la vista de entrenamientos
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="Volver",
                        width=280,
                        bgcolor="white",
                        on_click=go_back
                    ),
                    padding=ft.padding.only(20, 20)
                )
                # Agrega más botones según lo necesites...
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(20)
    )
    
    return nav

# Exportamos la función con el alias 'nav_buttons'
nav_buttons = nav_buttons

__all__ = ["nav_buttons"]
