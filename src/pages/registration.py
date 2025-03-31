import flet as ft
from utils.firebase import sign_up  # sign_up retorna el usuario creado o None
from pages.add_user_info import Add_user_info
from utils.global_state import auth_state

def registration_view(page: ft.Page):
    email_input = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.EMAIL,
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        width=300
    )
    confirm_email_input = ft.TextField(
        label="Confirmar correo electrónico",
        prefix_icon=ft.Icons.EMAIL,
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        width=300
    )
    password_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        width=300
    )

    # Botones con el estilo del segundo código
    register_button = ft.ElevatedButton(
        text="Registrar",
        height=50,
        width=250,
        color="#0F3BAC",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=5
        ),
        bgcolor="#FEF7FF",
        on_click=lambda e: register(e)
    )
    back_button = ft.ElevatedButton(
        text="Volver",
        bgcolor="#ffcccc",
        color="red",
        width=250,
        on_click=lambda e: go_back(e)
    )

    # Función para mostrar un diálogo de información
    def show_dialog(message, on_close=None):
        dlg = ft.AlertDialog(
            title=ft.Text("Información"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(e, dlg, on_close))
            ]
        )
        page.open(dlg)
        page.update()
    
    def close_dialog(e, dialog, on_close=None):
        dialog.open = False
        page.update()
        if on_close:
            on_close()
    
    # Función para manejar el registro (lógica del primer código)
    def register(e):
        email = email_input.value.strip()
        confirm_email = confirm_email_input.value.strip()
        password = password_input.value.strip()
        
        # Validación básica de los campos
        
        if email != confirm_email:
            show_dialog("Los correos electrónicos no coinciden.")
            return
        
        # Llama a sign_up; éste retorna el usuario creado o None
        user = sign_up(email, password)
        if user is not None:
            auth_state.is_authenticated = True
            auth_state.user = user
            def on_dialog_close():
                page.views.append(
                    ft.View(
                        route="/add_user_info",
                        controls=[Add_user_info(page)]
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
    
    # Construcción de la vista de registro con el estilo del segundo código
    registration_container = ft.Container(
        content=ft.Column(
            [
                ft.Column(
                    [
                        ft.Text("Registro", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                        ft.Text("Complete los campos para registrarse", size=16, color=ft.Colors.BLACK54)
                    ],
                    horizontal_alignment="center"
                ),
                ft.Column(
                    [
                        ft.Row(controls=[email_input], alignment="center"),
                        ft.Row(controls=[confirm_email_input], alignment="center"),
                        ft.Row(controls=[password_input], alignment="center")
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    [register_button, back_button],
                    spacing=20,
                    horizontal_alignment="center"
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        gradient=ft.LinearGradient(
            colors=[ft.Colors.WHITE, ft.Colors.BLUE_200],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        ),
        expand=True
    )
    
    return registration_container

# Exportamos la función con el alias "registration" para importarla desde main.py
Registration = registration_view

__all__ = ["registration"]
