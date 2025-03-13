import flet as ft
from controllers.main_controller import MainController

def main(page: ft.Page):
    page.title = "AST Tennis"
    page.bgcolor = ft.Colors.WHITE
    
    page.padding = 0
    page.horizontal_alignment = "stretch"
    page.vertical_alignment = "stretch"

    controller = MainController(page)
    controller.show_main_menu()

ft.app(target=main)
