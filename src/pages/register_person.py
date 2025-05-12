# src/pages/register_person.py

import flet as ft
import datetime
import re
from utils.ConexionDB import api_client

# Validation patterns
name_pattern    = re.compile(r"^[a-zA-Z\s]+$")
phone_pattern   = re.compile(r"^3\d{9}$")
address_pattern = re.compile(r"^(?=(?:[^#]*#){0,1}[^#]*$)(?=(?:[^-]*-){0,1}[^-]*$)[a-zA-Z0-9\s#-]+$")
email_pattern   = re.compile(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$")

def register_person_view(page: ft.Page):
    # — Back button —
    btn_back = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        tooltip="Volver",
        on_click=lambda e: page.go("/admin_menu")
    )

    # — Spinner —
    spinner = ft.ProgressRing(visible=False)

    # — Input fields —
    txt_nombre = ft.TextField(label="Nombre", width=300, prefix_icon=ft.Icons.ACCOUNT_BOX)
    txt_apellido = ft.TextField(label="Apellido", width=300, prefix_icon=ft.Icons.ACCOUNT_CIRCLE)
    txt_fecha = ft.TextField(
        label="Fecha de nacimiento",
        width=300,
        read_only=True,
        text_align=ft.TextAlign.CENTER,           # center-align date text
        prefix_icon=ft.Icons.CALENDAR_TODAY
    )
    txt_telefono = ft.TextField(label="Teléfono", width=300, prefix_icon=ft.Icons.PHONE)
    txt_direccion = ft.TextField(label="Dirección", width=300, prefix_icon=ft.Icons.HOME)
    txt_email = ft.TextField(label="Correo electrónico", width=300, prefix_icon=ft.Icons.EMAIL)
    txt_password = ft.TextField(
        label="Contraseña",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK
    )

    dropdown_categoria = ft.Dropdown(
        label="Categoría (si aplica)",
        width=300,
        options=[
            ft.dropdown.Option("Benjamin"),
            ft.dropdown.Option("Alevin"),
            ft.dropdown.Option("Infantil"),
            ft.dropdown.Option("Cadete"),
            ft.dropdown.Option("Intermedio"),
            ft.dropdown.Option("Avanzado"),
            ft.dropdown.Option("Profesional"),
        ]
    )
    dropdown_estado = ft.Dropdown(
        label="Estado",
        width=300,
        options=[
            ft.dropdown.Option("Registrado"),
            ft.dropdown.Option("Matriculado"),
            ft.dropdown.Option("No-Aplica"),
        ]
    )
    dropdown_rol = ft.Dropdown(
        label="Rol",
        width=300,
        hint_text="Seleccione rol",
        options=[
            ft.dropdown.Option("Usuario"),
            ft.dropdown.Option("Profesor"),
            ft.dropdown.Option("Administrador"),
        ]
    )

    # — Dialog helpers —
    def show_dialog(title, msg, on_close=None):
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(msg),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(e, dlg, on_close))]
        )
        page.open(dlg)
        page.update()

    def close_dialog(e, dlg, on_close=None):
        dlg.open = False
        page.update()
        if on_close:
            on_close()

    # — Date picker —
    def pick_date(e):
        today = datetime.date.today()
        dp = ft.DatePicker(
            first_date=today - datetime.timedelta(days=365*100),
            last_date=today,
            on_change=lambda e: [
                setattr(txt_fecha, "value", e.control.value.strftime("%Y-%m-%d")),
                page.update()
            ]
        )
        page.open(dp)

    # — Save handler —
    def save_person(e):
        # gather values
        nombre    = txt_nombre.value.strip()
        apellido  = txt_apellido.value.strip()
        fecha     = txt_fecha.value.strip()
        telefono  = txt_telefono.value.strip()
        direccion = txt_direccion.value.strip()
        email     = txt_email.value.strip()
        password  = txt_password.value.strip()
        categoria = dropdown_categoria.value or ""
        estado    = dropdown_estado.value or ""
        rol       = dropdown_rol.value or ""

        # validate
        if not all([nombre, apellido, fecha, telefono, direccion, email, password, estado, rol]):
            show_dialog("Error", "Debe completar todos los campos obligatorios.")
            return
        if not name_pattern.fullmatch(nombre):
            show_dialog("Error", "Nombre inválido.")
            return
        if not name_pattern.fullmatch(apellido):
            show_dialog("Error", "Apellido inválido.")
            return
        if not phone_pattern.fullmatch(telefono):
            show_dialog("Error", "Teléfono inválido.")
            return
        if not address_pattern.fullmatch(direccion):
            show_dialog("Error", "Dirección inválida.")
            return
        if not email_pattern.fullmatch(email):
            show_dialog("Error", "Correo inválido.")
            return
        # password length check
        if len(password) < 6:
            show_dialog("Error", "La contraseña debe tener al menos 6 caracteres.")
            return
        # date parse
        try:
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
        except:
            show_dialog("Error", "Formato de fecha debe ser YYYY-MM-DD.")
            return

        # call API
        spinner.visible = True
        page.update()
        data = {
            "email": email,
            "password": password,
            "rol": rol,
            "nombre": nombre,
            "apellido": apellido,
            "fechaNacimiento": fecha,
            "telefono": telefono,
            "direccion": direccion,
            "categoria": categoria,
            "estado": estado
        }
        try:
            api_client.post("personas/registrar", data=data)
            show_dialog("Éxito", f"Usuario {nombre} registrado.", on_close=lambda: page.go("/admin_menu"))
        except Exception as ex:
            show_dialog("Error", f"No se pudo registrar: {ex}")
        finally:
            spinner.visible = False
            page.update()

    # — Layout —
    content = ft.Column(
        controls=[
            ft.Row(
                controls=[btn_back, ft.Text("Registrar Persona", size=24)],
                alignment=ft.MainAxisAlignment.START
            ),
            txt_nombre,
            txt_apellido,
            ft.Row(
                controls=[
                    txt_fecha,
                    ft.ElevatedButton("Seleccionar fecha", on_click=pick_date)
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            txt_telefono,
            txt_direccion,
            txt_email,
            txt_password,                        # password field
            dropdown_categoria,
            dropdown_estado,
            dropdown_rol,
            ft.Container(spinner, alignment=ft.alignment.center),
            ft.ElevatedButton("Guardar", on_click=save_person, width=200)
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    return ft.Container(
        content=content,
        padding=20,
        gradient=ft.LinearGradient(
            colors=[ft.Colors.WHITE, ft.Colors.BLUE_100],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        ),
        expand=True
    )

# Export
Register_person = register_person_view
__all__ = ["register_person_view"]
