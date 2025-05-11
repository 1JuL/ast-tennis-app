import flet as ft
from models.event import Event, EventBuilder
from models.event_type import Event_Type, Event_TypeBuilder
import datetime
from utils.ConexionDB import api_client
import re

def gestionar_entrenamientos(page: ft.Page):
    entrenamientos_simulados = []
    profesores = []

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

    def obtener_profesores():
        try:
            response = api_client.get("personas")
            profesores = [persona for persona in response if persona['rol'] == 'Profesor']
            return profesores
        except Exception as e:
            print(f"Error al obtener los profesores: {e}")
            return []

    def obtener_entrenamientos():
        try:
            response = api_client.get("eventos")
            entrenamientos_tipo_2 = [evento for evento in response if evento.get('tipo') == 2]
            return entrenamientos_tipo_2
        except Exception as e:
            print(f"Error al obtener los eventos: {e}")
            return []

    def obtener_profesor_id(nombre_profesor):
        for profesor in profesores:
            if profesor['nombre'] == nombre_profesor:
                return profesor['id']
        return None

    def is_valid_time_range(start_time, end_time):
        try:
            start = datetime.datetime.strptime(start_time, '%H:%M')
            end = datetime.datetime.strptime(end_time, '%H:%M')
            return end > start
        except ValueError:
            return False

    def mostrar_formulario_crear(e):
        nombre_field = ft.TextField(label="Nombre del entrenamiento", hint_text="Nombre del entrenamiento", border_color=ft.Colors.BLUE_600)
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
        selected_start_time = ft.Text()
        selected_end_time = ft.Text()
        profesor_field = ft.Dropdown(
            label="Selecciona el nombre del profesor",
            options=[ft.dropdown.Option(profesor['nombre']) for profesor in profesores],
            width=300,
        )

        # Date Picker function
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

        # Time Pickers functions
        def pick_start_time(e):
            time_picker = ft.TimePicker(
                on_change=lambda e: [
                    setattr(selected_start_time, 'value', e.control.value.strftime("%H:%M")),
                    page.update()
                ]
            )
            page.overlay.append(time_picker)
            time_picker.open = True  # Set the open property to True
            page.update()

        def pick_end_time(e):
            time_picker = ft.TimePicker(
                on_change=lambda e: [
                    setattr(selected_end_time, 'value', e.control.value.strftime("%H:%M")),
                    page.update()
                ]
            )
            page.overlay.append(time_picker)
            time_picker.open = True  # Set the open property to True
            page.update()

        def guardar_entrenamiento(e):
            if not nombre_field.value or nombre_field.value.strip() == "":
                show_error_popup("El nombre del entrenamiento no puede estar vacío o contener solo espacios.")
                return

            if not categoria_field.value:
                show_error_popup("Debe seleccionar una categoría.")
                return

            if not selected_date.value:
                show_error_popup("Debe seleccionar una fecha.")
                return

            if not selected_start_time.value:
                show_error_popup("Debe seleccionar una hora de inicio.")
                return
            if not selected_end_time.value:
                show_error_popup("Debe seleccionar una hora de finalización.")
                return
            if not is_valid_time_range(selected_start_time.value, selected_end_time.value):
                show_error_popup("La hora final debe ser posterior a la hora inicial.")
                return

            if not profesor_field.value:
                show_error_popup("Debe seleccionar un profesor.")
                return
            profesor_id = obtener_profesor_id(profesor_field.value)
            if not profesor_id:
                show_error_popup("El profesor seleccionado no es válido.")
                return

            event_data = {
                'nombre': nombre_field.value.strip(),
                'categoria': categoria_field.value,
                'fecha': selected_date.value,
                'hora': selected_start_time.value,
                'horaFinal': selected_end_time.value,
                'tipo': 2,
                'profesorID': profesor_id,
                'podio': 0
            }

            try:
                response_evento = api_client.post("eventos", event_data)
                entrenamientos_existentes = obtener_entrenamientos()
                grid_entrenamientos.controls.clear()
                for entrenamiento in entrenamientos_existentes:
                    grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))

                dlg.open = False
                page.update()

            except Exception as err:
                show_error_popup(f"Error al guardar el entrenamiento: {err}")

        def cerrar_dialogo(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Crear Entrenamiento"),
            content=ft.Column(
                [
                    nombre_field,
                    categoria_field,
                    ft.Row([
                        ft.Text("Fecha:"),
                        selected_date,
                        ft.ElevatedButton("Seleccionar fecha", 
                                          on_click=pick_date,
                                          icon=ft.Icons.CALENDAR_MONTH),
                    ]),
                    ft.Row([
                        ft.Text("Hora inicio:"),
                        selected_start_time,
                        ft.ElevatedButton("Seleccionar hora",
                                          on_click=pick_start_time,
                                          icon=ft.Icons.ACCESS_TIME),
                    ]),
                    ft.Row([
                        ft.Text("Hora fin:"),
                        selected_end_time,
                        ft.ElevatedButton("Seleccionar hora",
                                          on_click=pick_end_time,
                                          icon=ft.Icons.ACCESS_TIME),
                    ]),
                    profesor_field,
                    ft.Row(
                        [
                            ft.ElevatedButton("Guardar", 
                                              on_click=guardar_entrenamiento, 
                                              color=ft.Colors.WHITE,
                                              bgcolor=ft.Colors.GREEN_700),
                            ft.ElevatedButton("Cancelar", 
                                              on_click=cerrar_dialogo,
                                              color=ft.Colors.WHITE,
                                              bgcolor=ft.Colors.RED_700),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=15,
                tight=True,
            ),
        )

        page.open(dlg)
        page.update()

    def mostrar_formulario_editar(entrenamiento):
        try:
            print(f"Opening edit form for entrenamiento: {entrenamiento}")  # Debug
            required_keys = ["id", "nombre", "categoria", "fecha", "hora"]
            missing_keys = [key for key in required_keys if key not in entrenamiento]
            if missing_keys:
                show_error_popup(f"Faltan datos en el entrenamiento: {missing_keys}")
                return

            print("Initializing form fields")  # Debug
            nombree_field = ft.TextField(
                label="Nombre del entrenamiento", 
                value=entrenamiento["nombre"], 
                border_color=ft.Colors.BLUE_600
            )
            categoriae_field = ft.Dropdown(
                width=300,
                value=entrenamiento["categoria"],
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
            selected_date_editar = ft.Text(value=entrenamiento["fecha"])
            selected_start_time_editar = ft.Text(value=entrenamiento["hora"])
            selected_end_time_editar = ft.Text(value=entrenamiento.get("horaFinal", "00:00"))

            print(f"Profesores available: {profesores}")  # Debug
            if not profesores:
                show_error_popup("No hay profesores disponibles.")
                return
            try:
                profesor_value = next((profesor['nombre'] for profesor in profesores 
                                    if profesor['id'] == entrenamiento.get('profesorID')), "")
                print(f"Selected professor value: {profesor_value}")  # Debug
            except Exception as e:
                print(f"Error setting professor value: {e}")
                show_error_popup("Error al cargar el profesor.")
                return
            profesore_field = ft.Dropdown(
                label="Selecciona el nombre del profesor",
                options=[ft.dropdown.Option(profesor['nombre']) for profesor in profesores],
                value=profesor_value,
                width=300,
            )

            print("Setting up pickers")  # Debug
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

            def pick_start_time(e):
                try:
                    initial_time = datetime.datetime.strptime(selected_start_time_editar.value, "%H:%M").time()
                except:
                    initial_time = datetime.time(12, 0)
                time_picker = ft.TimePicker(
                    value=initial_time,
                    on_change=lambda e: [
                        setattr(selected_start_time_editar, 'value', e.control.value.strftime("%H:%M")),
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

            def pick_end_time(e):
                try:
                    initial_time = datetime.datetime.strptime(selected_end_time_editar.value, "%H:%M").time()
                except:
                    initial_time = datetime.time(13, 0)
                time_picker = ft.TimePicker(
                    value=initial_time,
                    on_change=lambda e: [
                        setattr(selected_end_time_editar, 'value', e.control.value.strftime("%H:%M")),
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

            def guardar_edicion(e, entrenamiento_data=entrenamiento):  # Pass entrenamiento explicitly
                print("Saving edited entrenamiento")  # Debug
                if not nombree_field.value or nombree_field.value.strip() == "":
                    show_error_popup("El nombre del entrenamiento no puede estar vacío.")
                    return
                if not categoriae_field.value:
                    show_error_popup("Debe seleccionar una categoría.")
                    return
                if not selected_date_editar.value:
                    show_error_popup("Debe seleccionar una fecha.")
                    return
                if not selected_start_time_editar.value:
                    show_error_popup("Debe seleccionar una hora de inicio.")
                    return
                if not selected_end_time_editar.value:
                    show_error_popup("Debe seleccionar una hora de finalización.")
                    return
                if not is_valid_time_range(selected_start_time_editar.value, selected_end_time_editar.value):
                    show_error_popup("La hora final debe ser posterior a la hora inicial.")
                    return
                if not profesore_field.value:
                    show_error_popup("Debe seleccionar un profesor.")
                    return
                profesor_id = obtener_profesor_id(profesore_field.value)
                if not profesor_id:
                    show_error_popup("El profesor seleccionado no es válido.")
                    return

                event_data = {
                    'id': entrenamiento_data['id'],  # Use entrenamiento_data instead of entrenamiento
                    'nombre': nombree_field.value.strip(),
                    'categoria': categoriae_field.value,
                    'fecha': selected_date_editar.value,
                    'hora': selected_start_time_editar.value,
                    'horaFinal': selected_end_time_editar.value,
                    'tipo': 2,
                    'profesorID': profesor_id,
                    'podio': 0
                }

                try:
                    response_evento = api_client.put(f"eventos/{entrenamiento_data['id']}", event_data)
                    entrenamientos_existentes = obtener_entrenamientos()
                    grid_entrenamientos.controls.clear()
                    for evento in entrenamientos_existentes:  # Use a different variable name to avoid shadowing
                        grid_entrenamientos.controls.append(crear_card_entrenamiento(evento))
                    dlg.open = False
                    page.update()
                except Exception as err:
                    show_error_popup(f"Error al actualizar el entrenamiento: {err}")

            def cerrar_dialogo(e):
                print("Closing dialog")  # Debug
                dlg.open = False
                page.update()

            print("Creating dialog")  # Debug
            dlg = ft.AlertDialog(
                title=ft.Text("Editar Entrenamiento"),
                content=ft.Column(
                    [
                        nombree_field,
                        categoriae_field,
                        ft.Row([
                            ft.Text("Fecha:"),
                            selected_date_editar,
                            ft.ElevatedButton("Seleccionar fecha", 
                                on_click=pick_date,
                                icon=ft.Icons.CALENDAR_MONTH),
                        ]),
                        ft.Row([
                            ft.Text("Hora inicio:"),
                            selected_start_time_editar,
                            ft.ElevatedButton("Seleccionar hora",
                                on_click=pick_start_time,
                                icon=ft.Icons.ACCESS_TIME),
                        ]),
                        ft.Row([
                            ft.Text("Hora fin:"),
                            selected_end_time_editar,
                            ft.ElevatedButton("Seleccionar hora",
                                on_click=pick_end_time,
                                icon=ft.Icons.ACCESS_TIME),
                        ]),
                        profesore_field,
                        ft.Row(
                            [
                                ft.ElevatedButton("Guardar", 
                                    on_click=lambda e: guardar_edicion(e, entrenamiento),  # Pass entrenamiento
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREEN_700),
                                ft.ElevatedButton("Cancelar", 
                                    on_click=cerrar_dialogo,
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.RED_700),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    spacing=15,
                    tight=True,
                ),
            )   

            print("Opening dialog")  # Debug
            page.open(dlg)
            print("Dialog should be visible")  # Debug

        except Exception as err:
            print(f"Error in mostrar_formulario_editar: {err}")
            show_error_popup(f"Error al abrir el formulario de edición: {err}")   
    #dar formato a la card de cada entrenamiento
    def crear_card_entrenamiento(entrenamiento):
        profesor_id = entrenamiento.get('profesorID')
        profesor = next((profesor['nombre'] for profesor in profesores 
                       if profesor['id'] == profesor_id), "Desconocido") if profesor_id else "Desconocido"

        btn_modificar = ft.ElevatedButton(
            "Modificar", 
            on_click=lambda e: [
            print(f"Modificar clicked for entrenamiento: {entrenamiento}"),  # Debug print
            mostrar_formulario_editar(entrenamiento)
        ],  
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.AMBER_300
        )
        btn_eliminar = ft.ElevatedButton(
            "Eliminar", 
            on_click=lambda e: eliminar_entrenamiento(entrenamiento),
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_700
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(entrenamiento["nombre"], size=20, weight="bold"),
                        ft.Text(f"Fecha: {entrenamiento['fecha']}"),
                        ft.Text(f"Hora: {entrenamiento['hora']} - {entrenamiento.get('horaFinal', '')}"),
                        ft.Text(f"Categoría: {entrenamiento['categoria']}"),
                        ft.Text(f"Profesor: {profesor}"),
                        ft.Row([btn_modificar, btn_eliminar], 
                              spacing=10, 
                              alignment=ft.MainAxisAlignment.CENTER)
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

    def buscar_entrenamientos(e):
        filtro = search_field.value.lower()
        filtered_entrenamientos = [entrenamiento for entrenamiento in entrenamientos_existentes 
                                  if filtro in entrenamiento["nombre"].lower()]
        grid_entrenamientos.controls.clear()
        for entrenamiento in filtered_entrenamientos:
            grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))
        page.update()

    def eliminar_entrenamiento(entrenamiento):
        try:
            api_client.delete(f"eventos/{entrenamiento['id']}")
            entrenamientos_existentes = obtener_entrenamientos()
            grid_entrenamientos.controls.clear()
            for evento in entrenamientos_existentes:
                grid_entrenamientos.controls.append(crear_card_entrenamiento(evento))
            page.update()
        except Exception as e:
            show_error_popup(f"Error al eliminar el entrenamiento: {e}")

    def go_back(page):
        page.go("/admin_menu")

    # Initialize data
    profesores = obtener_profesores()
    entrenamientos_existentes = obtener_entrenamientos()

    # UI Components
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
        on_submit=buscar_entrenamientos
    )

    search_icon = ft.IconButton(
        icon=ft.Icons.SEARCH,
        icon_color=ft.Colors.BLUE_600,
        tooltip="Buscar",
        on_click=buscar_entrenamientos
    )
    search_container = ft.Row(
        controls=[
            search_field,
            search_icon
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START
    )

    btn_crear_entrenamiento = ft.ElevatedButton(
        "Nuevo Entrenamiento",
        on_click=mostrar_formulario_crear,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_600,
        icon=ft.Icons.ADD_CIRCLE_OUTLINE
    )

    toolbar = ft.Row(
        controls=[
            btn_volver,
            search_container,
            btn_crear_entrenamiento
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    grid_entrenamientos = ft.GridView(
        expand=True,
        max_extent=300,
        runs_count=3,
        spacing=15,
        run_spacing=15,
    )

    for evento in entrenamientos_existentes:
        grid_entrenamientos.controls.append(crear_card_entrenamiento(evento))

    main_container = ft.Column(
        controls=[
            toolbar,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            grid_entrenamientos
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

Gestionar_entrenamientos = gestionar_entrenamientos
__all__ = ["gestionar_entrenamientos"]