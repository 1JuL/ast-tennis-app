import flet as ft
import datetime
import re
from models.person import PersonBuilder  # Asegúrate de que la ruta sea correcta
from utils.global_state import auth_state
from pages.admin_menu import Admin_menu
from utils.ConexionDB import api_client  # Instancia global de APIClient

# Patrones de validación
name_pattern = re.compile(r"^[a-zA-Z\s]+$")  # Solo letras y espacios
phone_pattern = re.compile(r"^3\d{9}$")
address_pattern = re.compile(r"^(?=(?:[^#]*#){0,1}[^#]*$)(?=(?:[^-]*-){0,1}[^-]*$)[a-zA-Z0-9\s#-]+$")
email_pattern = re.compile(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$")

def add_user_info_view(page: ft.Page):
    # Obtén el email y el uid desde el estado global
    user = auth_state.user
    email = user.get("email", "") if user is not None else ""
    uid = user.get("localId", "") if user is not None else ""
    
    # Spinner de carga (oculto inicialmente)
    spinner = ft.ProgressRing(visible=False)
    
    # Campos de entrada para la información personal (ancho=300)
    txt_nombre = ft.TextField(
        label="Nombre",
        width=300,
        height=40,
        border="underline",
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        prefix_icon=ft.Icons.ACCOUNT_BOX
    )
    txt_apellido = ft.TextField(
        label="Apellido",
        width=300,
        height=40,
        border="underline",
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        prefix_icon=ft.Icons.ACCOUNT_CIRCLE
    )
    txt_fecha_nacimiento = ft.TextField(
        label="Fecha de nacimiento",
        width=300,
        height=40,
        border="underline",
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        prefix_icon=ft.Icons.CALENDAR_TODAY,
        read_only=True
    )
    txt_telefono = ft.TextField(
        label="Teléfono",
        width=300,
        height=40,
        border="underline",
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        prefix_icon=ft.Icons.PHONE
    )
    txt_direccion = ft.TextField(
        label="Dirección",
        width=300,
        height=40,
        border="underline",
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        prefix_icon=ft.Icons.HOME
    )
    txt_email = ft.TextField(
        label="Correo electrónico",
        width=300,
        height=40,
        border="underline",
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        prefix_icon=ft.Icons.EMAIL,
        value=email,
        read_only=True
    )
    dropdown_categoria = ft.Dropdown(
        width=300,
        hint_text="Categoría",
        hint_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        color="black",
        options=[
            ft.dropdown.Option("Benjamin"),
            ft.dropdown.Option("Alevin"),
            ft.dropdown.Option("Infantil"),
            ft.dropdown.Option("Cadete"),
            ft.dropdown.Option("Intermedio"),
            ft.dropdown.Option("Avanzado"),
            ft.dropdown.Option("Profesional")
        ]
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
        page.open(dlg)
        page.update()
    
    def close_dialog(e, dialog, on_close=None):
        dialog.open = False
        page.update()
        if on_close:
            on_close()
    
    # Función que abre el DatePicker de forma modal
    def pick_date(e):
        current_year = datetime.date.today().year
        first_date = datetime.date(current_year - 100, 1, 1)
        last_date = datetime.date(current_year - 6, 12, 31)
        
        def handle_date_change(e):
            if e.control.value:
                txt_fecha_nacimiento.value = e.control.value.strftime("%d/%m/%Y")
                page.update()
        
        dp = ft.DatePicker(
            first_date=first_date,
            last_date=last_date,
            on_change=handle_date_change,
            on_dismiss=lambda e: None
        )
        page.open(dp)
    
    def on_dialog_close():
        page.views.append(
            ft.View(
                route="/main_menu",
                controls=[Admin_menu(page)]
            )
        )
        page.go("/main_menu")
    
    # Función para guardar la información, enviar a la API y redirigir al main_menu
    def save_info(e):
        nombre = txt_nombre.value.strip()
        apellido = txt_apellido.value.strip()
        fecha_str = txt_fecha_nacimiento.value.strip()  # en formato dd/mm/yyyy
        telefono = txt_telefono.value.strip()
        direccion = txt_direccion.value.strip()
        email_val = txt_email.value.strip()
        categoria = dropdown_categoria.value or ""
        
        if not (nombre and apellido and fecha_str and telefono and direccion and email_val and categoria):
            show_dialog("Por favor, completa todos los campos obligatorios.")
            return

        if not name_pattern.fullmatch(nombre):
            show_dialog("El nombre solo puede contener letras y espacios.")
            return

        if not name_pattern.fullmatch(apellido):
            show_dialog("El apellido solo puede contener letras y espacios.")
            return

        if not phone_pattern.fullmatch(telefono):
            show_dialog("El teléfono debe tener 10 dígitos y comenzar con 3.")
            return
        else:
            if telefono[3] == "0" or telefono[4] == "0":
                show_dialog("El teléfono no puede tener ceros en el cuarto y quinto dígito.")
                return
            if re.search(r"0{4,}", telefono):
                show_dialog("El teléfono no puede tener más de 3 ceros seguidos.")
                return

        if not address_pattern.fullmatch(direccion):
            show_dialog("La dirección solo permite letras, números, espacios, # y -.")
            return

        if not email_pattern.fullmatch(email_val):
            show_dialog("Correo electrónico inválido.")
            return

        try:
            fecha_nacimiento = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except Exception as ex:
            show_dialog("Formato de fecha inválido. Utiliza dd/mm/yyyy.")
            return

        current_year = datetime.date.today().year
        if not (current_year - 100 <= fecha_nacimiento.year <= current_year - 6):
            show_dialog(f"La fecha de nacimiento debe estar entre {current_year - 100} y {current_year - 6}.")
            return

        today = datetime.date.today()
        age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        if categoria in ["Benjamin", "Alevin", "Infantil", "Cadete"]:
            if categoria == "Benjamin" and not (9 <= age <= 10):
                show_dialog("La edad no corresponde a la categoría Benjamin: 9–10 años.")
                return
            elif categoria == "Alevin" and not (11 <= age <= 12):
                show_dialog("La edad no corresponde a la categoría Alevin: 11–12 años.")
                return
            elif categoria == "Infantil" and not (13 <= age <= 14):
                show_dialog("La edad no corresponde a la categoría Infantil: 13–14 años.")
                return
            elif categoria == "Cadete" and not (15 <= age <= 16):
                show_dialog("La edad no corresponde a la categoría Cadete: 15–16 años.")
                return
        else:
            if age <= 16:
                show_dialog("Para la categoría seleccionada, la edad debe ser mayor a 16 años.")
                return

        fecha_nacimiento_str = fecha_nacimiento.isoformat()
        rol = "usuario"
        estado = "registrado"

        # Activa el spinner de carga
        spinner.visible = True
        page.update()
        
        data = {
            "nombre": nombre,
            "apellido": apellido,
            "fechaNacimiento": fecha_nacimiento_str,
            "telefono": telefono,
            "direccion": direccion,
            "email": email_val,
            "categoria": categoria,
            "estado": estado,
            "rol": rol,
            "uid": uid
        }
        
        try:
            api_client.post("personas", data=data)
            spinner.visible = True
            page.update()
            show_dialog("Información guardada exitosamente.", on_close=lambda: on_dialog_close())
        except Exception as ex:
            spinner.visible = False
            page.update()
            show_dialog("Error al guardar la información: " + str(ex))
    

    add_info_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Column(
                    [
                        ft.Text("Completa tu información", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, text_align="center"),
                        ft.Text("Por favor ingresa los datos solicitados", size=16, color=ft.Colors.BLACK54)
                    ],
                    horizontal_alignment="center"
                ),
                ft.Container(txt_nombre, padding=ft.padding.only(10)),
                ft.Container(txt_apellido, padding=ft.padding.only(10)),
                ft.Container(txt_fecha_nacimiento, padding=ft.padding.only(10)),
                ft.Container(
                    ft.ElevatedButton(
                        text="Seleccionar fecha",
                        height=30,
                        width=250,
                        color="#0F3BAC",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=5
                        ),
                        bgcolor="#FEF7FF",
                        on_click=pick_date
                    ),
                    padding=ft.padding.only(10)
                ),
                ft.Container(txt_telefono, padding=ft.padding.only(10)),
                ft.Container(txt_direccion, padding=ft.padding.only(10)),
                ft.Container(txt_email, padding=ft.padding.only(10)),
                ft.Container(dropdown_categoria, padding=ft.padding.only(10)),
                ft.Container(
                    ft.ElevatedButton(
                        text="Guardar",
                        height=40,
                        width=300,
                        color="#0F3BAC",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=5
                        ),
                        bgcolor="#FEF7FF",
                        on_click=save_info
                    ),
                    padding=ft.padding.only(20, 10)
                ),
                spinner  # Se muestra el spinner en la vista
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        expand=True,
        gradient=ft.LinearGradient(
            colors=[ft.Colors.WHITE, ft.Colors.BLUE_200],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        ),
        alignment=ft.alignment.center
    )

    return add_info_container

# Exportamos la vista con el alias Add_user_info para importarla desde main.py
Add_user_info = add_user_info_view
__all__ = ["add_user_info"]
