import flet as ft
from models.event import Event
from models.event_type import Event_Type, Event_TypeBuilder
import datetime
from utils.ConexionDB import api_client

def gestionar_torneos(page: ft.Page):
    profesores = []  # Lista de profesores, aunque profesorID es siempre 0 para torneos

    # Helper function to show error pop-up
    def show_error_popup(message):
        def close_popup(e):
            page.close(error_dialog)
            page.update()

        error_dialog = ft.AlertDialog(
            title=ft.Text("Error de Validación"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Aceptar", on_click=close_popup)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(error_dialog)
        page.update()

    # Fetch tournaments from API
    def obtener_torneos():
        try:
            response = api_client.get("eventos")
            torneos_tipo_1 = [evento for evento in response if evento.get('tipo') == 1]
            return torneos_tipo_1
        except Exception as e:
            show_error_popup(f"Error al obtener los torneos: {e}")
            return []

    # Fetch professors (for compatibility, though not used in tournaments)
    def obtener_profesores():
        try:
            response = api_client.get("personas")
            return [persona for persona in response if persona['rol'] == 'Profesor']
        except Exception as e:
            show_error_popup(f"Error al obtener los profesores: {e}")
            return []

    # Create tournament card
    def crear_card_torneo(torneo):
        profesor = "Sin profesor"  # Since profesorID is always 0 for tournaments
        btn_modificar = ft.ElevatedButton(
            "Modificar",
            on_click=lambda e: mostrar_formulario_editar(torneo),
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.AMBER_300
        )
        btn_eliminar = ft.ElevatedButton(
            "Eliminar",
            on_click=lambda e: eliminar_torneo(torneo),
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_700
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(torneo["nombre"], size=20, weight="bold"),
                        ft.Text(f"Fecha: {torneo['fecha']}"),
                        ft.Text(f"Hora: {torneo['hora']}"),
                        ft.Text(f"Categoría: {torneo['categoria']}"),
                        ft.Row([btn_modificar, btn_eliminar], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
                    ],
                    spacing=10
                ),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12)
            ),
            elevation=3,
            width=300
        )

    # Search tournaments
    def buscar_torneos(e):
        filtro = search_field.value.lower()
        filtered_torneos = [torneo for torneo in torneos_existentes if filtro in torneo["nombre"].lower()]
        grid_torneos.controls.clear()
        for torneo in filtered_torneos:
            grid_torneos.controls.append(crear_card_torneo(torneo))
        page.update()

    # Create tournament form
    def mostrar_formulario_crear(e):
        nombre_field = ft.TextField(label="Nombre del torneo", hint_text="Nombre del torneo", border_color=ft.Colors.BLUE_600)
        categoria_field = ft.Dropdown(
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
        selected_date = ft.Text()
        selected_time = ft.Text()

        def pick_date(e):
            date_picker = ft.DatePicker(
                first_date=datetime.date.today() - datetime.timedelta(days=365),
                last_date=datetime.date.today() + datetime.timedelta(days=365),
                on_change=lambda e: [
                    selected_date.__setattr__('value', e.control.value.strftime("%Y-%m-%d")),
                    page.update()
                ]
            )
            page.open(date_picker)

        def pick_time(e):
            time_picker = ft.TimePicker(
                on_change=lambda e: [
                    setattr(selected_time, 'value', e.control.value.strftime("%H:%M")),
                    page.overlay.remove(time_picker),
                    page.update()
                ],
                on_dismiss=lambda e: [
                    page.overlay.remove(time_picker),
                    page.update()
                ]
            )
            page.overlay.append(time_picker)
            time_picker.open = True
            page.update()

        def guardar_torneo(e, dialog):
            if not nombre_field.value or nombre_field.value.strip() == "":
                show_error_popup("El nombre del torneo no puede estar vacío o contener solo espacios.")
                return
            if not categoria_field.value:
                show_error_popup("Debe seleccionar una categoría.")
                return
            if not selected_date.value:
                show_error_popup("Debe seleccionar una fecha.")
                return
            if not selected_time.value:
                show_error_popup("Debe seleccionar una hora.")
                return

            try:
                fecha = datetime.datetime.strptime(selected_date.value, '%Y-%m-%d').date()
                hora = datetime.datetime.strptime(selected_time.value, '%H:%M').time()
                torneo_data = {
                    "nombre": nombre_field.value.strip(),
                    "fecha": str(fecha),
                    "hora": str(hora),
                    "tipo": 1,
                    "categoria": categoria_field.value,
                    "profesorID": 0,
                    "podio": 0
}

                api_client.post("eventos", torneo_data)
                grid_torneos.controls.clear()
                for torneo in obtener_torneos():
                    grid_torneos.controls.append(crear_card_torneo(torneo))
                dialog.open = False
                page.update()
            except ValueError as ve:
                show_error_popup("Formato de fecha u hora inválido.")
            except Exception as err:
                show_error_popup(f"Error al guardar el torneo: {err}")

        def cerrar_dialogo(e, dialog):
            dialog.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Crear Torneo"),
            content=ft.Column(
                [
                    nombre_field,
                    categoria_field,
                    ft.Row([
                        ft.Text("Fecha:"),
                        selected_date,
                        ft.ElevatedButton("Seleccionar fecha", on_click=pick_date, icon=ft.Icons.CALENDAR_MONTH)
                    ]),
                    ft.Row([
                        ft.Text("Hora:"),
                        selected_time,
                        ft.ElevatedButton("Seleccionar hora", on_click=pick_time, icon=ft.Icons.ACCESS_TIME)
                    ]),
                    ft.Row(
                        [
                            ft.ElevatedButton("Guardar", on_click=lambda e: guardar_torneo(e, dlg), color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_700),
                            ft.ElevatedButton("Cancelar", on_click=lambda e: cerrar_dialogo(e, dlg), color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_700)
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=15,
                tight=True
            )
        )

        page.open(dlg)
        page.update()

    # Edit tournament form
    def mostrar_formulario_editar(torneo):
        required_keys = ["id", "nombre", "categoria", "fecha", "hora"]
        missing_keys = [key for key in required_keys if key not in torneo]
        if missing_keys:
            show_error_popup(f"Faltan datos en el torneo: {missing_keys}")
            return

        nombree_field = ft.TextField(label="Nombre del torneo", value=torneo["nombre"], border_color=ft.Colors.BLUE_600)
        categoriae_field = ft.Dropdown(
            width=300,
            value=torneo["categoria"],
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
        selected_date_editar = ft.Text(value=torneo["fecha"])
        selected_time_editar = ft.Text(value=torneo["hora"])

        def pick_date(e):
            try:
                initial_date = datetime.datetime.strptime(selected_date_editar.value, "%Y-%m-%d").date()
            except:
                initial_date = datetime.date.today()
            date_picker = ft.DatePicker(
                value=initial_date,
                first_date=datetime.date.today() - datetime.timedelta(days=365),
                last_date=datetime.date.today() + datetime.timedelta(days=365),
                on_change=lambda e: [
                    setattr(selected_date_editar, 'value', e.control.value.strftime("%Y-%m-%d")),
                    page.update()
                ]
            )
            page.open(date_picker)

        def pick_time(e):
            try:
                initial_time = datetime.datetime.strptime(selected_time_editar.value, "%H:%M").time()
            except:
                initial_time = datetime.time(12, 0)
            time_picker = ft.TimePicker(
                value=initial_time,
                on_change=lambda e: [
                    setattr(selected_time_editar, 'value', e.control.value.strftime("%H:%M")),
                    page.overlay.remove(time_picker),
                    page.update()
                ],
                on_dismiss=lambda e: [
                    page.overlay.remove(time_picker),
                    page.update()
                ]
            )
            page.overlay.append(time_picker)
            time_picker.open = True
            page.update()

        def guardar_edicion(e, dialog, torneo_data=torneo):
            if not nombree_field.value or nombree_field.value.strip() == "":
                show_error_popup("El nombre del torneo no puede estar vacío.")
                return
            if not categoriae_field.value:
                show_error_popup("Debe seleccionar una categoría.")
                return
            if not selected_date_editar.value:
                show_error_popup("Debe seleccionar una fecha.")
                return
            if not selected_time_editar.value:
                show_error_popup("Debe seleccionar una hora.")
                return

            try:
                fecha = datetime.datetime.strptime(selected_date_editar.value, '%Y-%m-%d').date()
                hora = datetime.datetime.strptime(selected_time_editar.value, '%H:%M').time()
                
                torneo_data = {
                    "id": torneo_data['id'],
                    "nombre": nombree_field.value.strip(),
                    "fecha": str(fecha),
                    "hora": str(hora),
                    "tipo": 1,
                    "categoria": categoriae_field.value,
                    "profesorID": 0,
                    "podio": 0
                }

                api_client.put(f"eventos/{torneo_data['id']}", torneo_data)
                grid_torneos.controls.clear()
                for torneo in obtener_torneos():
                    grid_torneos.controls.append(crear_card_torneo(torneo))
                dialog.open = False
                page.update()
            except ValueError as ve:
                show_error_popup("Formato de fecha u hora inválido.")
            except Exception as err:
                show_error_popup(f"Error al actualizar el torneo: {err}")

        def cerrar_dialogo(e, dialog):
            dialog.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Editar Torneo"),
            content=ft.Column(
                [
                    nombree_field,
                    categoriae_field,
                    ft.Row([
                        ft.Text("Fecha:"),
                        selected_date_editar,
                        ft.ElevatedButton("Seleccionar fecha", on_click=pick_date, icon=ft.Icons.CALENDAR_MONTH)
                    ]),
                    ft.Row([
                        ft.Text("Hora:"),
                        selected_time_editar,
                        ft.ElevatedButton("Seleccionar hora", on_click=pick_time, icon=ft.Icons.ACCESS_TIME)
                    ]),
                    ft.Row(
                        [
                            ft.ElevatedButton("Guardar", on_click=lambda e: guardar_edicion(e, dlg, torneo), color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_700),
                            ft.ElevatedButton("Cancelar", on_click=lambda e: cerrar_dialogo(e, dlg), color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_700)
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=15,
                tight=True
            )
        )

        page.open(dlg)
        page.update()

    # Delete tournament
    def eliminar_torneo(torneo):
        try:
            api_client.delete(f"eventos/{torneo['id']}")
            grid_torneos.controls.clear()
            for torneo in obtener_torneos():
                grid_torneos.controls.append(crear_card_torneo(torneo))
            page.update()
        except Exception as e:
            show_error_popup(f"Error al eliminar el torneo: {e}")

    # Initialize data
    profesores = obtener_profesores()
    torneos_existentes = obtener_torneos()

    # UI Components
    def go_back(page):
        page.go("/admin_menu")
            
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: go_back(page)
    )

    search_field = ft.TextField(
        hint_text="Filtrar por nombre de torneo",
        width=300,
        color=ft.Colors.BLACK,
        hint_style=ft.TextStyle(color=ft.Colors.BLACK54),
        border_color=ft.Colors.BLUE_600,
        on_submit=buscar_torneos
    )

    search_icon = ft.IconButton(
        icon=ft.Icons.SEARCH,
        icon_color=ft.Colors.BLUE_600,
        tooltip="Buscar",
        on_click=buscar_torneos
    )
    search_container = ft.Row(
        controls=[
            search_field,
            search_icon
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START
    )

    btn_crear_torneo = ft.ElevatedButton(
        "Nuevo Torneo",
        on_click=mostrar_formulario_crear,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_600,
        icon=ft.Icons.ADD_CIRCLE_OUTLINE
    )

    toolbar = ft.Row(
        controls=[
            btn_volver,
            search_container,
            btn_crear_torneo
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
    grid_torneos = ft.GridView(
        expand=True,
        max_extent=300,
        runs_count=3,
        spacing=15,
        run_spacing=15
    )

    for torneo in torneos_existentes:
        grid_torneos.controls.append(crear_card_torneo(torneo))

    main_container = ft.Column(
        controls=[
            toolbar,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            grid_torneos
        ],
        expand=True,
        spacing=10
    )

    return ft.Container(
        content=main_container,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.WHITE, ft.Colors.BLUE_100]
        ),
        expand=True,
        padding=20
    )

Gestionar_torneos = gestionar_torneos
__all__ = ["gestionar_torneos"]