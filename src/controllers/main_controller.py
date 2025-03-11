import flet as ft
from views.main_view import MainView
from views.registration_view import RegistrationView

class MainController:
    def __init__(self, page: ft.Page):
        self.page = page
        
    def show_main_menu(self):
        self.page.clean()  # Limpia la página de elementos anteriores
        main_menu = MainView(self)
        self.page.add(main_menu.view)
        self.page.update()
        
    def go_to_registration(self):
        self.page.clean()
        self.page.bgcolor= ft.colors.BLACK
        self.page.vertical_alignment="center"
        self.page.horizontal_alignment= "center"
        
        registration_view = RegistrationView(self)
        self.page.add(registration_view.view)
        self.page.update()
        
    # Aquí puedes agregar más métodos para navegar a otros componentes
