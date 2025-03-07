import flet as ft
from controllers.main_controller import MainController

def main(page: ft.Page):
    page.title = "AST Tennis"
    # Creamos el controlador principal, que se encargará de la navegación
    controller = MainController(page)
    # Mostramos el menú principal
    controller.show_main_menu()

ft.app(target=main)
