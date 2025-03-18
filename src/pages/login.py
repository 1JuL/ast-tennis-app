import flet as ft

def login_view(page: ft.Page):
    # Definición de los campos de entrada para el login
    txt_email = ft.TextField(
        width=280,
        height=40,
        hint_text="Correo electrónico",
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

    def close_dialog(e, dlg):
        dlg.open = False
        page.update()

    # Función para manejar el inicio de sesión
    def handle_login(e):
        email = txt_email.value
        password = txt_password.value
        if not email or not password:
            show_dialog("Todos los campos son obligatorios.")
            return
        # Aquí podrías agregar la lógica de autenticación real.
        show_dialog("¡Inicio de sesión exitoso!")

    # Función para volver al menú principal
    def go_back(e):
        if hasattr(page, "on_back"):
            page.on_back()
        else:
            page.clean()
            page.update()

    # Construcción de la vista de login
    login_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    ft.Text(
                        "Iniciar sesión",
                        width=320,
                        size=30,
                        text_align="center",
                        weight="w900"
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(txt_email, padding=ft.padding.only(20, 20)),
                ft.Container(txt_password, padding=ft.padding.only(20, 20)),
                ft.Container(
                    ft.ElevatedButton(
                        text="Iniciar sesión",
                        width=280,
                        bgcolor="black",
                        on_click=handle_login
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

    return login_container

# "Exportamos" la función con el alias 'login'
Login = login_view

__all__ = ["login"]
