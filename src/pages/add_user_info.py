import flet as ft
import datetime
from models.person import PersonBuilder  # Asegúrate de que la ruta sea correcta
from utils.global_state import auth_state

def add_user_info_view(page: ft.Page):
    # Obtén el email desde el estado global
    user = auth_state.user
    email = user.get("email", "") if user is not None else ""
    
    # Campos de entrada para la información personal
    txt_nombre = ft.TextField(
        width=280,
        height=40,
        hint_text="Nombre",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.ACCOUNT_BOX
    )
    txt_apellido = ft.TextField(
        width=280,
        height=40,
        hint_text="Apellido",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.ACCOUNT_CIRCLE
    )
    txt_fecha_nacimiento = ft.TextField(
        width=280,
        height=40,
        hint_text="Fecha de nacimiento (dd/mm/yyyy)",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.CALENDAR_TODAY
    )
    txt_telefono = ft.TextField(
        width=280,
        height=40,
        hint_text="Teléfono",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.PHONE
    )
    txt_direccion = ft.TextField(
        width=280,
        height=40,
        hint_text="Dirección",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.HOME
    )
    # Campo de email, prellenado y de solo lectura
    txt_email = ft.TextField(
        width=280,
        height=40,
        hint_text="Correo electrónico",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.EMAIL,
        value=email,
        read_only=True
    )
    txt_categoria = ft.TextField(
        width=280,
        height=40,
        hint_text="Categoría",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.CATEGORY
    )
    txt_estado = ft.TextField(
        width=280,
        height=40,
        hint_text="Estado",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.CHECK_CIRCLE
    )
    txt_rol = ft.TextField(
        width=280,
        height=40,
        hint_text="Rol",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.ADMIN_PANEL_SETTINGS
    )

    # Función para mostrar un diálogo de información usando page.open()
    def show_dialog(message):
        dlg = ft.AlertDialog(
            title=ft.Text("Información"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(e, dlg))
            ]
        )
        page.open(dlg)
        page.update()
    
    def close_dialog(e, dialog):
        dialog.open = False
        page.update()
    
    # Función para guardar la información y crear el objeto Person
    def save_info(e):
        nombre = txt_nombre.value
        apellido = txt_apellido.value
        fecha_str = txt_fecha_nacimiento.value
        telefono = txt_telefono.value
        direccion = txt_direccion.value
        email_val = txt_email.value
        categoria = txt_categoria.value
        estado = txt_estado.value
        rol = txt_rol.value

        # Validación básica
        if not (nombre and apellido and fecha_str and telefono and direccion and email_val):
            show_dialog("Por favor, completa todos los campos obligatorios.")
            return

        try:
            fecha_nacimiento = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except Exception as ex:
            show_dialog("Formato de fecha inválido. Utiliza dd/mm/yyyy.")
            return

        # Construir el objeto Person usando PersonBuilder
        person = (
            PersonBuilder()
            .set_nombre(nombre)
            .set_apellido(apellido)
            .set_fecha_nacimiento(fecha_nacimiento)
            .set_telefono(telefono)
            .set_direccion(direccion)
            .set_email(email_val)
            .set_categoria(categoria)
            .set_estado(estado)
            .set_rol(rol)
            .build()
        )

        # Aquí puedes guardar el objeto person (por ejemplo, en Firebase o en otra base de datos)
        show_dialog("Información guardada exitosamente.")

    def go_back(e):
        if hasattr(page, "on_back"):
            page.on_back()
        else:
            page.clean()
            page.update()

    add_info_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    ft.Text("Completa tu información", size=30, weight="w900", text_align="center"),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(txt_nombre, padding=ft.padding.only(10)),
                ft.Container(txt_apellido, padding=ft.padding.only(10)),
                ft.Container(txt_fecha_nacimiento, padding=ft.padding.only(10)),
                ft.Container(txt_telefono, padding=ft.padding.only(10)),
                ft.Container(txt_direccion, padding=ft.padding.only(10)),
                ft.Container(txt_email, padding=ft.padding.only(10)),
                ft.Container(txt_categoria, padding=ft.padding.only(10)),
                ft.Container(txt_estado, padding=ft.padding.only(10)),
                ft.Container(txt_rol, padding=ft.padding.only(10)),
                ft.Container(
                    ft.ElevatedButton(
                        text="Guardar",
                        width=280,
                        bgcolor="black",
                        on_click=save_info
                    ),
                    padding=ft.padding.only(20, 10)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        border_radius=20,
        width=400,
        height=700,
        gradient=ft.LinearGradient(
            colors=[ft.Colors.PURPLE, ft.Colors.PINK, ft.Colors.RED]
        ),
        alignment=ft.alignment.center
    )

    return add_info_container

# Exportamos la vista con el alias Add_user_info para importarla desde main.py
Add_user_info = add_user_info_view
__all__ = ["add_user_info"]
