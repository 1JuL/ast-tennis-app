import flet as ft
from utils.firebase import sign_up  # sign_up retorna el usuario creado o None
from pages.add_user_info import Add_user_info
from utils.global_state import auth_state

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
    
    # Función para mostrar un diálogo de información usando page.open(dlg)
    def show_dialog(message, on_close=None):
        dlg = ft.AlertDialog(
            title=ft.Text("Información"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(e, dlg, on_close))
            ]
        )
        page.open(dlg)  # Abre el diálogo usando el helper method recomendado
        page.update()
    
    def close_dialog(e, dialog, on_close=None):
        dialog.open = False
        page.update()
        if on_close:
            on_close()
    
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
        
        # Llama a sign_up; éste retorna el usuario creado o None
        user = sign_up(email, password)
        if user is not None:
            # Registro exitoso: actualiza el estado global
            auth_state.is_authenticated = True
            auth_state.user = user
            def on_dialog_close():
                # Agrega la vista de add_user_info sin pasar email, ya que se obtiene del estado global
                page.views.append(
                    ft.View(
                        route="/add_user_info",
                        controls=[ Add_user_info(page) ]
                    )
                )
                page.go("/add_user_info")
            show_dialog("¡Registro exitoso!", on_close=on_dialog_close)
        else:
            show_dialog("Error en el registro.")
    
    # Función para volver al menú principal
    def go_back(e):
        if hasattr(page, "on_back"):
            page.on_back()
        else:
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

# Exportamos la función con el alias "registration" para importarla desde main.py
Registration = registration_view

__all__ = ["registration"]
