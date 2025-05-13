import flet as ft
import requests
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

    # Fetch authorized participants for a tournament (asistencia: true)
    def obtener_participantes_autorizados(torneo_id):
        try:
            response = api_client.get("personasEventos", params={"eventoId": torneo_id, "asistencia": "true"})
            print(f"Participantes autorizados para torneo {torneo_id}: {response}")  # Depuración
            return response if response else []
        except Exception as e:
            show_error_popup(f"Error al obtener participantes autorizados: {e}")
            return []

    # Update participant's authorization status
    def actualizar_autorizacion(participante_id, asistencia):
        try:
            response = api_client.put(
                f"personasEventos/{participante_id}",
                data={"asistencia": asistencia}
            )
            page.snack_bar = ft.SnackBar(ft.Text("Autorización actualizada"), bgcolor=ft.Colors.GREEN_600)
            page.snack_bar.open = True
            page.update()
        except requests.exceptions.HTTPError as e:
            show_error_popup(f"Error al actualizar autorización: {e.response.status_code}")
        except Exception as e:
            show_error_popup(f"Error al actualizar autorización: {e}")

    # Show dialog to manage participants
    def mostrar_participantes(torneo):
        participantes = obtener_participantes_torneo(torneo['id'])
        lista = ft.ListView(expand=True, spacing=10, padding=10)

        if not participantes:
            lista.controls.append(ft.Text("No hay participantes inscritos", italic=True, color=ft.Colors.GREY_600))
        else:
            for participante in participantes:
                lista.controls.append(
                    ft.ListTile(
                        title=ft.Text(
                            f"{participante.get('persona', {}).get('nombre', 'Desconocido')} {participante.get('persona', {}).get('apellido', '')}",
                            weight="bold"
                        ),
                        trailing=ft.Switch(
                            value=participante.get('asistencia', False),
                            on_change=lambda e, pid=participante['id']: actualizar_autorizacion(pid, e.control.value)
                        )
                    )
                )

        dialog = ft.AlertDialog(
            title=ft.Text(f"Participantes: {torneo['nombre']}"),
            content=ft.Container(content=lista, height=300, width=400, bgcolor=ft.Colors.WHITE),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialog), style=ft.ButtonStyle(color=ft.Colors.BLUE_700))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(dialog)
        page.update()

    # Fetch all participants for a tournament (including those with asistencia: false)
    def obtener_participantes_torneo(torneo_id):
        try:
            response = api_client.get("personasEventos", params={"eventoId": torneo_id})
            return response if response else []
        except Exception as e:
            show_error_popup(f"Error al obtener participantes: {e}")
            return []

    # Update podium for a tournament
    def actualizar_podio(torneo_id, podio):
        try:
            response = api_client.put(
                f"eventos/{torneo_id}",
                data={"podio": podio}
            )
            print(f"Respuesta de la API al actualizar podio: {response}")  # Depuración
            page.snack_bar = ft.SnackBar(ft.Text("Podio actualizado correctamente."), bgcolor=ft.Colors.GREEN_600)
            page.snack_bar.open = True
            page.update()
            return True
        except requests.exceptions.HTTPError as e:
            show_error_popup(f"Error al actualizar podio: {e.response.status_code}")
            return False
        except Exception as e:
            show_error_popup(f"Error al actualizar podio: {e}")
            return False

    # Show dialog to edit podium
    def mostrar_formulario_podio(torneo):
        participantes = obtener_participantes_autorizados(torneo['id'])
        if not participantes:
            show_error_popup("No hay participantes autorizados para este torneo.")
            return

        # Crear opciones para los dropdowns (participantes con asistencia: true)
        opciones = [
            ft.dropdown.Option(key=None, text="Ninguno")
        ] + [
            ft.dropdown.Option(key=p['personaUid'], text=f"{p['persona'].get('nombre', 'Desconocido')} {p['persona'].get('apellido', '')}")
            for p in participantes if p.get('persona') and p['persona'].get('nombre')
        ]

        # Convertir podio a diccionario si es un entero (0)
        podio_actual = torneo.get('podio', {})
        if isinstance(podio_actual, int):
            podio_actual = {"primero": None, "segundo": None, "tercero": None}

        # Campos de dropdown para cada puesto, con valores actuales del podio si existen
        primer_puesto = ft.Dropdown(
            label="Primer Puesto",
            options=opciones,
            value=podio_actual.get('primero'),
            width=300
        )
        segundo_puesto = ft.Dropdown(
            label="Segundo Puesto",
            options=opciones,
            value=podio_actual.get('segundo'),
            width=300
        )
        tercer_puesto = ft.Dropdown(
            label="Tercer Puesto",
            options=opciones,
            value=podio_actual.get('tercero'),
            width=300
        )

        def guardar_podio(e):
            podio = {
                "primero": primer_puesto.value,
                "segundo": segundo_puesto.value,
                "tercero": tercer_puesto.value
            }
            if actualizar_podio(torneo['id'], podio):
                page.close(dialog)

        dialog = ft.AlertDialog(
            title=ft.Text(f"Editar Podio - {torneo['nombre']}"),
            content=ft.Column([
                primer_puesto,
                segundo_puesto,
                tercer_puesto,
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog)),
                ft.TextButton("Guardar", on_click=guardar_podio),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(dialog)
        page.update()

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
        btn_participantes = ft.ElevatedButton(
            "Gestionar Participantes",
            on_click=lambda e: mostrar_participantes(torneo),
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600
        )
        btn_podio = ft.ElevatedButton(
            "Podio",
            on_click=lambda e: mostrar_formulario_podio(torneo),
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.PURPLE_600
        )

        # Convertir podio a diccionario si es un entero (0)
        podio = torneo.get('podio', {})
        if isinstance(podio, int):
            podio = {"primero": None, "segundo": None, "tercero": None}

        # Mostrar el podio actual si existe
        podio_text = []
        if podio.get('primero'):
            participante = next((p for p in obtener_participantes_autorizados(torneo['id']) if p['personaUid'] == podio['primero']), None)
            nombre = participante['persona'].get('nombre', 'Desconocido') if participante else "Desconocido"
            podio_text.append(f"1º: {nombre}")
        if podio.get('segundo'):
            participante = next((p for p in obtener_participantes_autorizados(torneo['id']) if p['personaUid'] == podio['segundo']), None)
            nombre = participante['persona'].get('nombre', 'Desconocido') if participante else "Desconocido"
            podio_text.append(f"2º: {nombre}")
        if podio.get('tercero'):
            participante = next((p for p in obtener_participantes_autorizados(torneo['id']) if p['personaUid'] == podio['tercero']), None)
            nombre = participante['persona'].get('nombre', 'Desconocido') if participante else "Desconocido"
            podio_text.append(f"3º: {nombre}")

        content = [
            ft.Text(torneo["nombre"], size=20, weight="bold"),
            ft.Text(f"Fecha: {torneo['fecha']}"),
            ft.Text(f"Hora: {torneo['hora']}"),
            ft.Text(f"Categoría: {torneo['categoria']}"),
            ft.Text(f"Capacidad: {torneo.get('num_personas', 'No especificado')}"),
        ]

        if podio_text:
            content.append(ft.Text("Podio:", weight="bold", color=ft.Colors.PURPLE_800))
            for linea in podio_text:
                content.append(ft.Text(linea, color=ft.Colors.GREY_800))

        content.append(
            ft.Row(
                [btn_modificar, btn_eliminar, btn_participantes, btn_podio],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
            )
        )

        return ft.Card(
            elevation=3,
            width=300,
             # wrap content in a container that expands and centers its child
            content=ft.Container(
                expand=True,                                    # fill the card
                alignment=ft.alignment.center,                  # center the Column
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
                content=ft.Column(
                    controls=content,                          # your list of Text/Row
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,     # center vertically
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER  # center horizontally
                )
            )
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
        cupos_field = ft.TextField(label="Cupos del torneo", hint_text="Cupos del torneo", border_color=ft.Colors.BLUE_600)
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
            if not cupos_field.value or not cupos_field.value.isdigit():
                show_error_popup("El número de cupos debe ser un número entero positivo.")
                return
            if int(cupos_field.value) <= 0:
                show_error_popup("El número de cupos debe ser mayor que 0.")
                return
            if not categoria_field.value or categoria_field.value == "":
                show_error_popup("Debe seleccionar una categoría.")
                return
            if not selected_date.value:
                show_error_popup("Debe seleccionar una fecha.")
                return
            try:
                fecha = datetime.datetime.strptime(selected_date.value, '%Y-%m-%d').date()
                if fecha < datetime.date.today():
                    show_error_popup("La fecha debe ser igual o posterior a la fecha actual.")
                    return
            except ValueError:
                show_error_popup("Formato de fecha inválido.")
                return
            if fecha > datetime.date.today() + datetime.timedelta(days=365):
                show_error_popup("La fecha debe ser menor a un año.")
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
                    "horaFinal": 0,
                    "tipo": 1,
                    "categoria": categoria_field.value,
                    "profesorID": 0,
                    "podio": {"primero": None, "segundo": None, "tercero": None},  # Inicializar como diccionario
                    "num_personas": int(cupos_field.value)
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
                    cupos_field,
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
        required_keys = ["id", "nombre", "num_personas", "categoria", "fecha", "hora"]
        missing_keys = [key for key in required_keys if key not in torneo]
        if missing_keys:
            show_error_popup(f"Faltan datos en el torneo: {missing_keys}")
            return

        nombree_field = ft.TextField(label="Nombre del torneo", value=torneo["nombre"], border_color=ft.Colors.BLUE_600)
        cupose_field = ft.TextField(label="Cupos del torneo", value=str(torneo["num_personas"]), border_color=ft.Colors.BLUE_600)
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
            if not cupose_field.value or not cupose_field.value.isdigit():
                show_error_popup("El número de cupos debe ser un número entero positivo.")
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
                
                # Convertir podio a diccionario si es un entero
                podio = torneo_data.get('podio', {})
                if isinstance(podio, int):
                    podio = {"primero": None, "segundo": None, "tercero": None}

                torneo_data = {
                    "id": torneo_data['id'],
                    "nombre": nombree_field.value.strip(),
                    "fecha": str(fecha),
                    "hora": str(hora),
                    "tipo": 1,
                    "categoria": categoriae_field.value,
                    "profesorID": 0,
                    "podio": podio,
                    "num_personas": int(cupose_field.value)
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
                    cupose_field,
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

    def cerrar_dialogo(dialog):
        dialog.open = False
        page.update()

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
        max_extent=550,
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