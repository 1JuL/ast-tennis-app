import flet as ft
from views.main_view import MainView
from views.login_view import LoginView
from views.registration_view import RegistrationView

class MainController:
    def __init__(self, page: ft.Page):
        self.page = page
        
    def show_main_menu(self):
        self.page.clean()
        self.page.vertical_alignment="stretch"
        self.page.horizontal_alignment= "stretch"
        main_menu = MainView(self)
        self.page.controls = [main_menu.view]
        self.page.update()

    def go_to_login(self):
        self.page.bgcolor=ft.Colors.BLACK
        self.page.vertical_alignment="center"
        self.page.horizontal_alignment= "center"

        login_view = LoginView(self)
        self.page.controls = [login_view.view]
        self.page.update()
        
    def go_to_registration(self):
        self.page.bgcolor= ft.Colors.BLACK
        self.page.vertical_alignment="center"
        self.page.horizontal_alignment= "center"
        
        registration_view = RegistrationView(self)
        self.page.controls = [registration_view.view]
        self.page.update()
        
    # Aquí puedes agregar más métodos para navegar a otros componentes
