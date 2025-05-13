import flet as ft
import datetime
import re
from utils.ConexionDB import api_client
from utils.global_state import auth_state

# Patrones de validación
name_pattern = re.compile(r"^[a-zA-Z\s]+$")  # Solo letras y espacios
phone_pattern = re.compile(r"^3\d{9}$")
address_pattern = re.compile(r"^(?=(?:[^#]*#){0,1}[^#]*$)(?=(?:[^-]*-){0,1}[^-]*$)[a-zA-Z0-9\s#-]+$")
email_pattern = re.compile(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$")

def edit_person_modal(page: ft.Page, person: dict):
    # Convertir la fecha de ISO (yyyy-mm-dd) a dd/mm/yyyy
    fecha_iso = person.get("fechaNacimiento", "2000-01-01")
    try:
        fecha_dt = datetime.datetime.strptime(fecha_iso, "%Y-%m-%d").date()
        fecha_str = fecha_dt.strftime("%d/%m/%Y")
    except Exception:
        fecha_str = ""
    
    txt_nombre = ft.TextField(label="Nombre", value=person.get("nombre", ""), width=300)
    txt_apellido = ft.TextField(label="Apellido", value=person.get("apellido", ""), width=300)
    txt_fecha = ft.TextField(
        label="Fecha de nacimiento",
        width=300,
        height=40,
        border="underline",
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
        prefix_icon=ft.Icons.CALENDAR_TODAY,
        value=fecha_str,
        read_only=True
    )
    txt_telefono = ft.TextField(label="Teléfono", value=person.get("telefono", ""), width=300)
    txt_direccion = ft.TextField(label="Dirección", value=person.get("direccion", ""), width=300)
    txt_email = ft.TextField(label="Correo electrónico", value=person.get("email", ""), width=300, read_only=True)
    
    dropdown_categoria = ft.Dropdown(
        label="Categoría",
        width=300,
        value=person.get("categoria", ""),
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
    
    dropdown_estado = ft.Dropdown(
        label="Estado",
        width=300,
        value=person.get("estado", ""),
        options=[
            ft.dropdown.Option("matriculado"),
            ft.dropdown.Option("registrado")
        ]
    )
    
    # Función que abre el DatePicker de forma modal y actualiza txt_fecha
    def pick_date(e):
        current_year = datetime.date.today().year
        first_date = datetime.date(current_year - 100, 1, 1)
        last_date = datetime.date(current_year - 6, 12, 31)
        
        def handle_date_change(e):
            if e.control.value:
                txt_fecha.value = e.control.value.strftime("%d/%m/%Y")
                page.update()
        
        dp = ft.DatePicker(
            first_date=first_date,
            last_date=last_date,
            on_change=handle_date_change,
            on_dismiss=lambda e: None
        )
        page.open(dp)
    
    # Botón para seleccionar fecha
    btn_pick_date = ft.ElevatedButton(
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
    )
    
    # Función para cerrar el modal de edición
    def close_edit(e, dlg):
        dlg.open = False
        page.update()
    
    # Función para guardar la edición, validar y hacer PUT
    def save_edit(e, dlg):
        nombre = txt_nombre.value.strip()
        apellido = txt_apellido.value.strip()
        fecha_str_new = txt_fecha.value.strip()  # Formato dd/mm/yyyy
        telefono = txt_telefono.value.strip()
        direccion = txt_direccion.value.strip()
        email_val = txt_email.value.strip()
        categoria = dropdown_categoria.value or ""
        estado = dropdown_estado.value or ""
        
        # Validaciones básicas y con expresiones regulares
        if not (nombre and apellido and fecha_str_new and telefono and direccion and email_val and categoria):
            show_dialog(page, "Por favor, completa todos los campos obligatorios.")
            return

        if not name_pattern.fullmatch(nombre):
            show_dialog(page, "El nombre solo puede contener letras y espacios.")
            return

        if not name_pattern.fullmatch(apellido):
            show_dialog(page, "El apellido solo puede contener letras y espacios.")
            return

        if not phone_pattern.fullmatch(telefono):
            show_dialog(page, "El teléfono debe tener 10 dígitos y comenzar con 3.")
            return
        else:
            if telefono[3] == "0" or telefono[4] == "0":
                show_dialog(page, "El teléfono no puede tener ceros en el cuarto y quinto dígito.")
                return
            if re.search(r"0{4,}", telefono):
                show_dialog(page, "El teléfono no puede tener más de 3 ceros seguidos.")
                return

        if not address_pattern.fullmatch(direccion):
            show_dialog(page, "La dirección solo permite letras, números, espacios, # y -.")
            return

        if not email_pattern.fullmatch(email_val):
            show_dialog(page, "Correo electrónico inválido.")
            return

        try:
            fecha_nacimiento = datetime.datetime.strptime(fecha_str_new, "%d/%m/%Y").date()
        except Exception:
            show_dialog(page, "Formato de fecha inválido. Utiliza dd/mm/yyyy.")
            return

        current_year = datetime.date.today().year
        if not (current_year - 100 <= fecha_nacimiento.year <= current_year - 6):
            show_dialog(page, f"La fecha de nacimiento debe estar entre {current_year - 100} y {current_year - 6}.")
            return

        today = datetime.date.today()
        age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        # Validación de la categoría en función de la edad
        if categoria in ["Benjamin", "Alevin", "Infantil", "Cadete"]:
            if categoria == "Benjamin" and not (9 <= age <= 10):
                show_dialog(page, "La edad no corresponde a la categoría Benjamin: 9–10 años.")
                return
            elif categoria == "Alevin" and not (11 <= age <= 12):
                show_dialog(page, "La edad no corresponde a la categoría Alevin: 11–12 años.")
                return
            elif categoria == "Infantil" and not (13 <= age <= 14):
                show_dialog(page, "La edad no corresponde a la categoría Infantil: 13–14 años.")
                return
            elif categoria == "Cadete" and not (15 <= age <= 16):
                show_dialog(page, "La edad no corresponde a la categoría Cadete: 15–16 años.")
                return
        else:
            if age <= 16:
                show_dialog(page, "Para la categoría seleccionada, la edad debe ser mayor a 16 años.")
                return

        fecha_iso_new = fecha_nacimiento.isoformat()
        data = {
            "nombre": nombre,
            "apellido": apellido,
            "fechaNacimiento": fecha_iso_new,
            "telefono": telefono,
            "direccion": direccion,
            "email": email_val,
            "categoria": categoria,
            "estado": estado
        }
        try:
            response = api_client.put(f"personas/{person.get('id')}", data=data)
            dlg.open = False
            page.update()
            show_dialog(page, "Información actualizada exitosamente.")
        except Exception as ex:
            show_dialog(page, "Error al actualizar: " + str(ex))
    
    dlg = ft.AlertDialog(
        title=ft.Text("Editar información"),
        content=ft.Column(
            controls=[
                txt_nombre,
                txt_apellido,
                txt_fecha,
                btn_pick_date,
                txt_telefono,
                txt_direccion,
                txt_email,
                dropdown_categoria,
                dropdown_estado
            ],
            spacing=10
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: close_edit(e, dlg)),
            ft.TextButton("Guardar", on_click=lambda e: save_edit(e, dlg))
        ]
    )
    page.open(dlg)
    page.update()
    
# Función para mostrar un diálogo de información
def show_dialog(page: ft.Page, message, on_close=None):
    dlg = ft.AlertDialog(
        title=ft.Text("Información"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("OK", on_click=lambda e: close_dialog(page, dlg, on_close))
        ]
    )
    page.open(dlg)
    page.update()

def close_dialog(page: ft.Page, dialog, on_close=None):
    dialog.open = False
    page.update()
    if on_close:
        on_close()  

def logout(page: ft.Page):
    # Clear global auth state
    auth_state.is_authenticated = False
    auth_state.user = None
    # Navigate away
    page.go("/")
    page.update()

def admin_menu_view(page: ft.Page):
    
    # Función para mostrar los detalles de una persona en un diálogo
    def show_person_details(person):
        details = (
            f"Fecha de nacimiento: {person.get('fechaNacimiento', '')}\n"
            f"Teléfono: {person.get('telefono', '')}\n"
            f"Dirección: {person.get('direccion', '')}\n"
            f"Email: {person.get('email', '')}\n"
            f"Categoría: {person.get('categoria', '')}"
        )
        dlg = ft.AlertDialog(
            title=ft.Text("Detalles de la persona"),
            content=ft.Text(details),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: close_dialog(page, dlg))
            ]
        )
        page.open(dlg)
        page.update()

    # Sidebar con botones de navegación y "Salir"
    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                ft.ElevatedButton(
                    text="Gestionar Entrenamientos",
                    width=250,
                    on_click=lambda _: page.go("/gestionar_entrenamientos")
                ),
                
                ft.ElevatedButton(
                    text="Gestionar Torneos",
                    width=250,
                    on_click=lambda _: page.go("/gestionar_torneos")
                ),
                
                
                
                ft.ElevatedButton(
                    text="Gestionar Pagos",
                    width=250,
                    on_click=lambda _: page.go("/gestionar_pagos")
                ),
                
                ft.ElevatedButton(
                    text="Visualizar Entrenamientos",
                    width=250,
                    on_click=lambda _: page.go("/visualizar_entrenamientos")
                ),
                
                ft.ElevatedButton(
                    text="Visualizar Torneos",
                    width=250,
                    on_click=lambda _: page.go("/visualizar_torneos")
                ),
                
                ft.ElevatedButton(
                    text="Trainer Trainings",
                    width=250,
                    on_click=lambda _: page.go("/trainer_trainings")
                ),
                
                ft.ElevatedButton(
                    text="Register Person",
                    width=250,
                    on_click=lambda _: page.go("/register_person")
                ),
                
                ft.Divider(color=ft.Colors.WHITE54),
                
                ft.ElevatedButton(
                    "Logout",
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: logout(page)
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=250,
        bgcolor=ft.Colors.BLUE_GREY,
        padding=ft.padding.all(15)
    )

    # Función para crear una tarjeta (card) para cada persona
    def person_card(person):
        full_name = f"{person.get('nombre', '')} {person.get('apellido', '')}"
        estado = person.get("estado", "Desconocido")
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(full_name, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Email: {person.get('email', '')}"),
                        ft.Text(f"Estado: {estado}"),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Editar",
                                    width=80,
                                    bgcolor=ft.Colors.YELLOW_700,
                                    color=ft.Colors.WHITE,
                                    on_click=lambda e, p=person: edit_person_modal(page, p)
                                ),
                                ft.ElevatedButton(
                                    text="Ver detalles",
                                    width=100,
                                    bgcolor=ft.Colors.BLUE,
                                    color=ft.Colors.WHITE,
                                    on_click=lambda e, p=person: show_person_details(p)
                                ),
                                ft.ElevatedButton(
                                    text="Eliminar",
                                    width=80,
                                    bgcolor=ft.Colors.RED,
                                    color=ft.Colors.WHITE,
                                    on_click=lambda e, p=person: print("Eliminar", p)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ],
                    spacing=10
                ),
                padding=ft.padding.all(10),
            ),
            width=300,
        )
        return card

    # Obtener datos del usuario logueado para la bienvenida
    uid = auth_state.user.get("localId", "") if auth_state.user else ""
    try:
        logged_in_response = api_client.get(f"personas/uid/{uid}")
        if isinstance(logged_in_response, list) and logged_in_response:
            logged_in_person = logged_in_response[0]
        else:
            logged_in_person = logged_in_response
        welcome_name = logged_in_person.get("nombre", "Usuario")
    except Exception as ex:
        print("Error al obtener datos del usuario:", ex)
        welcome_name = "Administrador"

    # Obtener todas las personas mediante GET al endpoint "personas"
    try:
        persons = api_client.get("personas")
    except Exception as ex:
        print("Error al obtener personas:", ex)
        persons = []

    cards = []
    if persons:
        for person in persons:
            cards.append(person_card(person))
    else:
        cards.append(ft.Text("No se encontraron personas."))

    grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=400,
        spacing=10,
        child_aspect_ratio=1.0,
        run_spacing=10,
        controls=cards
    )

    # Contenido principal: mensaje de bienvenida (con nombre del usuario) y grid de tarjetas
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(f"Bienvenido, {welcome_name}", size=30, weight=ft.FontWeight.BOLD, text_align="center"),
                grid
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        gradient= ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_200], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
        expand=True,
        alignment=ft.alignment.center
    )
    
    return ft.Container(
        expand=True,
        content=ft.Column([
            ft.Row(controls=[sidebar, main_content], expand=True),
        ])
    )

Admin_menu = admin_menu_view
__all__ = ["admin_menu"]
