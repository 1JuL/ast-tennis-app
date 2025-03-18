import flet as ft
from utils.firebase import sign_in
from utils.global_state import auth_state  # Importa la instancia global

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
    
    # Spinner de carga
    spinner = ft.ProgressRing(visible=False)
    
    def handle_login(e):
        # Mostrar spinner de carga
        spinner.visible = True
        page.update()
        
        email = txt_email.value
        password = txt_password.value
        
        # Realiza la autenticación
        user = sign_in(email, password)
        
        # Ocultar spinner de carga
        spinner.visible = False
        page.update()
        
        if user:
            print("Usuario autenticado:", user)
            # Actualiza el estado global
            auth_state.is_authenticated = True
            auth_state.user = user
            dlg = ft.AlertDialog(
                title=ft.Text("Éxito"),
                content=ft.Text("Inicio de sesión exitoso"),
                actions=[]
            )
            # Agrega la acción, ya que dlg ya existe
            dlg.actions.append(
                ft.TextButton("OK", on_click=lambda e: close_dialog(e, dlg))
            )
        else:
            print("Error al iniciar sesión")
            # Actualiza el estado global en caso de error
            auth_state.is_authenticated = False
            auth_state.user = None
            dlg = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("No se pudo iniciar sesión"),
                actions=[]
            )
            dlg.actions.append(
                ft.TextButton("OK", on_click=lambda e: close_dialog(e, dlg))
            )
        # Abre el diálogo usando el helper method recomendado
        page.open(dlg)
    
    def close_dialog(e, dialog):
        dialog.open = False
        page.update()
        
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
                        text_align=ft.TextAlign.CENTER,
                        weight="w900"
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(txt_email, padding=ft.padding.only(20, 20)),
                ft.Container(txt_password, padding=ft.padding.only(20, 20)),
                ft.Container(spinner, alignment=ft.alignment.center, padding=ft.padding.only(10)),
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
