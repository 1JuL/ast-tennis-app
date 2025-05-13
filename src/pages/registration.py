# src/pages/registration.py

import flet as ft
from utils.firebase        import sign_up
from utils.global_state    import auth_state

def registration_view(page: ft.Page):
    # Inputs
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

    # Buttons
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
        bgcolor="red",
        height=50,
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
        width=250,
        on_click=lambda e: page.go("/")   # back to home
    )

    # Dialog helpers
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

    # Registration logic
    def register(e):
        email        = email_input.value.strip()
        confirm_email = confirm_email_input.value.strip()
        password     = password_input.value.strip()
        
        if not email or not confirm_email or not password:
            show_dialog("Todos los campos son obligatorios.")
            return

        if email != confirm_email:
            show_dialog("Los correos electrónicos no coinciden.")
            return
        
        user = sign_up(email, password)
        if user:
            auth_state.is_authenticated = True
            auth_state.user = user

            # On success, navigate to add_user_info
            def on_ok():
                page.go("/add_user_info")

            show_dialog("¡Registro exitoso!", on_close=on_ok)

        else:
            show_dialog("Error en el registro.")

    # UI layout
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

# Export
Registration = registration_view
__all__ = ["registration"]
