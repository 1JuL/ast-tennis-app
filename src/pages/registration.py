import flet as ft
from utils.firebase import sign_up  # sign_up retorna el usuario creado o None
from pages.add_user_info import Add_user_info
from utils.global_state import auth_state

def registration_view(page: ft.Page):
    # Definición de los campos de entrada
    name_input = ft.TextField(label="Nombre", prefix_icon=ft.Icons.PERSON, color='black', width=300)
    lastname_input = ft.TextField(label="Apellido", prefix_icon=ft.Icons.PERSON, color='black', width=300)
    birthdate_input = ft.TextField(label="Fecha de nacimiento", prefix_icon=ft.Icons.CALENDAR_MONTH, color='black', width=300)
    phone_input = ft.TextField(label="Teléfono", prefix_icon=ft.Icons.PHONE, color='black', width=300)
    address_input = ft.TextField(label="Dirección", prefix_icon=ft.Icons.HOME, color='black', width=300)
    email_input = ft.TextField(label="Correo", prefix_icon=ft.Icons.EMAIL, color='black', width=300)
    password_input = ft.TextField(label="Contraseña", password=True, prefix_icon=ft.Icons.LOCK, color='black', width=300)

    #botones

    login_button = ft.ElevatedButton(
                                text="Registrarse",
                                height=50,
                                width=250,
                                color='#0F3BAC',
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation=5
                                ),
                                bgcolor='#FEF7FF',
                                on_click=lambda _: register
                            )
    back_button = ft.ElevatedButton("Volver", bgcolor="#ffcccc", color="red", width=250, on_click=lambda _: go_back)
    
    
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
        user_data = {
            "nombre": name_input.value.strip(),
            "apellido": lastname_input.value.strip(),
            "fecha": birthdate_input.value.strip(),
            "telefono": phone_input.value.strip(),
            "direccion": address_input.value.strip(),
            "email": email_input.value.strip(),
            "password": password_input.value.strip(),
        }

        # Validar que ningún campo esté vacío
        for campo, valor in user_data.items():
            if not valor:  # Si está vacío
                show_dialog("Complete todos los campos")
                return  
        
        # Llama a sign_up; éste retorna el usuario creado o None
        user = sign_up(user_data["email"], user_data["password"])
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
    def go_back():
        if hasattr(page, "on_back"):
            page.on_back()
        else:
            page.clean()
            page.update()
    
    # Construcción de la vista de registro
    registration_container = ft.Container(
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
                        ft.Row(controls=[name_input], alignment='center'),
                        ft.Row(controls=[lastname_input], alignment='center'),
                        ft.Row(controls=[birthdate_input], alignment='center'),
                        ft.Row(controls=[phone_input], alignment='center'),
                        ft.Row(controls=[address_input], alignment='center'),
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
    
    return registration_container

# Exportamos la función con el alias "registration" para importarla desde main.py
Registration = registration_view

__all__ = ["registration"]
