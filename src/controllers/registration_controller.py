import flet as ft
from views.main_view import MainView

class RegistrationController:
    def __init__(self, view):
        self.view = view
        
    def register(self, e):
        username = self.view.txt_username.value
        email = self.view.txt_email.value
        password = self.view.txt_password.value
        
        # Validación básica de los campos
        if not username or not email or not password:
            self.show_dialog("Todos los campos son obligatorios.")
            return
        
        # Aquí podrías agregar la lógica para guardar el usuario o llamar a un servicio.
        self.show_dialog("¡Registro exitoso!")
        
    def show_dialog(self, message):
        page = self.view.controller.page  # ✅ Se obtiene correctamente la referencia a la página
        dlg = ft.AlertDialog(
            title=ft.Text("Información"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog(e, dlg))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
        
    def close_dialog(self, e, dialog):
        dialog.open = False
        self.view.controller.page.update()

