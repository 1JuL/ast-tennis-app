import flet as ft
from utils.firebase import sign_in
from utils.global_state import auth_state
from pages.admin_menu import Admin_menu

def login_view(page: ft.Page):
    # Definición de los campos de entrada para el login
    email_input = ft.TextField(
        label="Correo", 
        prefix_icon=ft.Icons.EMAIL, 
        color= 'black',
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
    )
    password_input = ft.TextField(
        label="Contraseña", 
        password=True, 
        prefix_icon=ft.Icons.LOCK, 
        color= ft.Colors.BLACK,
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
    )

    login_button = ft.ElevatedButton(
        text="Iniciar Sesión",
        height=50,
        width=250,
        color='#0F3BAC',
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=5
        ),
        bgcolor='#FEF7FF',
        on_click=lambda e: handle_login(e)
    )
    back_button = ft.ElevatedButton("Volver", bgcolor="#ffcccc", color="red", width=250, on_click= lambda e: go_back(e))
    
    
    # Spinner de carga
    spinner = ft.ProgressRing(visible=False)
    
    def handle_login(e):
        # Mostrar spinner de carga
        spinner.visible = True
        page.update()
        
        email = email_input.value
        password = password_input.value
        
        # Realiza la autenticación
        user = sign_in(email, password)
        
        # Ocultar spinner de carga
        spinner.visible = False
        page.update()
        
        if user:
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
                ft.TextButton("OK", on_click=lambda e: close_dialog_success(e, dlg))
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
    
    def close_dialog_success(e, dialog):
        dialog.open = False
        page.update()
        page.views.append(
            ft.View(
                route="/main_menu",
                controls=[Admin_menu(page)]
            )
        )
        page.go("/main_menu")
        
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
                ft.Column(
                    [
                        ft.Text("Iniciar sesión", size=32, weight=ft.FontWeight.BOLD,color=ft.Colors.BLACK),
                        ft.Text("Hola de nuevo", size=16, color=ft.Colors.BLACK54)
                    ],
                    horizontal_alignment= 'center'
                ),
                ft.Column(
                    [
                        ft.Row(controls=[email_input], alignment='center'),
                        ft.Row(controls=[password_input], alignment='center')
                    ],
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    [login_button, back_button]
                )
                
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand= True
        ),
        gradient= ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_200], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
        expand=True,
    )
    
    return login_container


Login = login_view

__all__ = ["login"]
