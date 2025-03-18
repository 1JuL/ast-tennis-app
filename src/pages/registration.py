import flet as ft

def registration_view(page: ft.Page):
    # Definición de los campos de entrada
    txt_username = ft.TextField(
        width=280,
        height=40,
        hint_text="Nombre de usuario",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.PERSON
    )
    txt_email = ft.TextField(
        width=280,
        height=40,
        hint_text="Correo electrónico",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.EMAIL
    )
    txt_confirm_email = ft.TextField(
        width=280,
        height=40,
        hint_text="Confirmar correo electrónico",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.EMAIL
    )
    txt_password = ft.TextField(
        width=280,
        height=40,
        hint_text="Contraseña",
        border="underline",
        color="black",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK
    )
    
    # Función para mostrar un diálogo de información
    def show_dialog(message):
        dlg = ft.AlertDialog(
            title=ft.Text("Información"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(e, dlg))
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    def close_dialog(e, dialog):
        dialog.open = False
        page.update()
    
    # Función para manejar el registro
    def register(e):
        username = txt_username.value
        email = txt_email.value
        confirm_email = txt_confirm_email.value
        password = txt_password.value
        
        # Validación básica de los campos
        if not username or not email or not confirm_email or not password:
            show_dialog("Todos los campos son obligatorios.")
            return
        
        if email != confirm_email:
            show_dialog("Los correos electrónicos no coinciden.")
            return
        
        # Aquí podrías agregar la lógica para guardar el usuario o llamar a un servicio.
        show_dialog("¡Registro exitoso!")
    
    # Función para volver al menú principal
    def go_back(e):
        # Se asume que la página tiene un callback on_back asignado por el componente principal
        if hasattr(page, "on_back"):
            page.on_back()
        else:
            # Por defecto, se limpia la página
            page.clean()
            page.update()
    
    # Construcción de la vista de registro
    registration_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    ft.Text(
                        "Registro",
                        width=320,
                        size=30,
                        text_align="center",
                        weight="w900"
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(txt_username, padding=ft.padding.only(20, 20)),
                ft.Container(txt_email, padding=ft.padding.only(20, 20)),
                ft.Container(txt_confirm_email, padding=ft.padding.only(20, 20)),
                ft.Container(txt_password, padding=ft.padding.only(20, 20)),
                ft.Container(
                    ft.ElevatedButton(
                        text="Registrar",
                        width=280,
                        bgcolor="black",
                        on_click=register
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="Volver",
                        width=280,
                        bgcolor="black",
                        on_click=go_back
                    ),
                    padding=ft.padding.only(20, 20)
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        border_radius=20,
        width=320,
        height=500,
        gradient=ft.LinearGradient(
            colors=[ft.Colors.PURPLE, ft.Colors.PINK, ft.Colors.RED]
        )
    )
    
    return registration_container

# Exportamos la función con el nombre "registration" para importarla desde main.py
Registration = registration_view

# Opcional: definir __all__ para dejar claro qué se exporta al usar "from pages.registration import *"
__all__ = ["registration"]
