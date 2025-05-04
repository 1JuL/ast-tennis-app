import flet as ft
from models.event import Event, EventBuilder
from models.event_type import Event_Type, Event_TypeBuilder
import datetime
from utils.ConexionDB import api_client  # Asegúrate de tener la configuración correcta para api_client

def gestionar_torneos(page: ft.Page):

    torneos_simulados = []  # Lista donde almacenaremos los torneos creados

    # Lista de profesores: La obtendremos de la API (si se necesita para algún propósito, aunque ya no se usará el ID)
    profesores = []

    # Función común para procesar los formularios (creación y edición)
    def procesar_torneo(event_data, page, dlg, is_creacion=True):
        try:
            # Validar fecha
            fecha = datetime.datetime.strptime(event_data['fecha'], '%d/%m/%Y').date()
            hora = datetime.datetime.strptime(event_data['hora'], '%H:%M').time()

            # Crear un evento usando el EventBuilder
            event = EventBuilder()\
                .set_nombre(event_data['nombre'])\
                .set_fecha(fecha)\
                .set_hora(hora)\
                .set_tipo(event_data['categoria'])\
                .build()

            torneo_data = {
                "nombre": event.nombre,
                "fecha": str(event.fecha),
                "hora": str(event.hora),
                "tipo": 1,  # Tipo siempre es 1 para torneos
                "categoria": event_data['categoria'],
                "profesorID": 0,  # ProfesorID siempre es 0
                "podio": 0  # Mandamos 0 explícitamente en el campo podio
            }

            # Crear o actualizar el torneo
            if is_creacion:
                response_torneo = api_client.post("eventos", torneo_data)  # Usamos /eventos para los torneos
            else:
                response_torneo = api_client.put(f"eventos/{event_data['id']}", torneo_data)  # Usamos /eventos/{id}

            # Recargar los torneos después de la creación o edición
            torneos_existentes = obtener_torneos()
            grid_torneos.controls.clear()
            for torneo in torneos_existentes:
                grid_torneos.controls.append(crear_card_torneo(torneo))

            page.controls.remove(dlg)
            page.update()

        except ValueError as ex:
            print("Error en formato de fecha u hora:", ex)

    # Función para crear tarjeta de torneo
    def crear_card_torneo(torneo):
        # Verificar si el campo 'profesorID' existe en el torneo
        profesor_id = torneo.get('profesorID')

        if profesor_id:
            # Buscar el nombre del profesor usando el profesorID
            profesor = next((profesor['nombre'] for profesor in profesores if profesor['id'] == profesor_id), "Desconocido")
        else:
            profesor = "Desconocido"

        # Definir los botones dentro de la función
        btn_modificar = ft.ElevatedButton("Modificar", on_click=lambda e: mostrar_formulario_editar(torneo), color=ft.Colors.YELLOW_600)
        btn_eliminar = ft.ElevatedButton("Eliminar", on_click=lambda e: eliminar_torneo(torneo), color=ft.Colors.RED_600)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(torneo["nombre"], size=20, weight="bold"),
                        ft.Text(f"Fecha: {torneo['fecha']}"),
                        ft.Text(f"Hora: {torneo['hora']}"),
                        ft.Text(f"Categoría: {torneo['categoria']}"),  # Mostramos la categoría
                        ft.Row([btn_modificar, btn_eliminar], spacing=10, alignment=ft.MainAxisAlignment.CENTER)  # Usamos los botones aquí
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

    # Función para obtener los torneos existentes desde la API
    def obtener_torneos():
        try:
            response = api_client.get("eventos")  # La ruta sigue siendo /eventos
            # Filtrar solo los torneos cuyo tipo sea 1
            torneos_tipo_1 = [evento for evento in response if evento.get('tipo') == 1]
            return torneos_tipo_1
        except Exception as e:
            print(f"Error al obtener los eventos: {e}")
            return []

    # Función para volver al menú o la vista anterior
    def go_back(page):
        if hasattr(page, "on_back"):
            page.on_back()
        else:
            page.clean()
            page.update()

    # Función de búsqueda
    def buscar_torneos(e):
        filtro = search_field.value.lower()
        filtered_torneos = [torneo for torneo in torneos_existentes if filtro in torneo["nombre"].lower()]

        # Limpiar y agregar tarjetas filtradas
        grid_torneos.controls.clear()
        for torneo in filtered_torneos:
            grid_torneos.controls.append(crear_card_torneo(torneo))
        page.update()

    # Función para crear un nuevo torneo
    def mostrar_formulario_crear(e):
        nombre_field = ft.TextField(label="Nombre del torneo", hint_text="Nombre del torneo")
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
        fecha_field = ft.TextField(label="Fecha del torneo", hint_text="aaaa-mm-dd")
        hora_field = ft.TextField(label="Hora del torneo", hint_text="hh:mm")

        def guardar_torneo(e):
            # Solo enviar los datos esenciales
            event_data = {
                'nombre': nombre_field.value,
                'categoria': categoria_field.value,
                'fecha': fecha_field.value,
                'hora': hora_field.value,
                'tipo': 1,  # Todos los torneos son de tipo 1
                'profesorID': 0,  # ProfesorID siempre es 0
                'podio': 0  # Enviamos el valor 0 en el campo podio
            }

            # Llamar a la API para crear el evento
            try:
                response_torneo = api_client.post("eventos", event_data)  # Usamos /eventos para los torneos
                print("Respuesta de la API:", response_torneo)

                torneos_existentes = obtener_torneos()
                grid_torneos.controls.clear()
                for torneo in torneos_existentes:
                    grid_torneos.controls.append(crear_card_torneo(torneo))
                page.update()

                page.controls.remove(dlg)
                page.update()

            except Exception as err:
                print(f"Other error occurred: {err}")

        def cerrar_dialogo(e):
            page.controls.remove(dlg)
            page.update()

        dlg = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Crear Torneo", size=20, weight="bold"),
                    nombre_field,
                    categoria_field,
                    fecha_field,
                    hora_field,
                    ft.Row(
                        [
                            ft.ElevatedButton("Guardar", on_click=guardar_torneo, color=ft.Colors.BLUE_600),
                            ft.ElevatedButton("Cancelar", on_click=cerrar_dialogo, color=ft.Colors.RED_400),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=15,
                tight=True,
            ),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            width=400,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12),
        )

        page.controls.append(dlg)
        page.update()

    # Función para modificar un torneo
    def mostrar_formulario_editar(torneo):
        nombre_field = ft.TextField(label="Nombre del torneo", hint_text="Ingresa el nombre", value=torneo["nombre"])
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
        fecha_field = ft.TextField(label="Fecha del torneo", hint_text="aaaa-mm-dd", value=torneo["fecha"])
        hora_field = ft.TextField(label="Hora del torneo", hint_text="hh:mm", value=torneo["hora"])

        print("Torneo a editar:", torneo)
        id_edición = torneo["id"]
        print("ID de edición:", id_edición)

        def guardar_torneo(e, id_edicion):    
            # Ahora 'torneo' está disponible aquí
            print("Torneo a editar:", torneo)
            
            event_data = {
                'id': id_edición,  # El ID del torneo que se está editando
                'nombre': nombre_field.value,
                'categoria': categoria_field.value,
                'fecha': fecha_field.value,
                'hora': hora_field.value,
                'tipo': 1,  # Todos los torneos son de tipo 1
                'profesorID': 0,  # ProfesorID siempre es 0
                'podio': 0  # Enviamos el valor 0 en el campo podio
            }

            # Llamar a la API para actualizar el evento
            try:
                response_torneo = api_client.put(f"eventos/{torneo['id']}", event_data)  # Usamos /eventos
                print("Respuesta de la API:", response_torneo)

                torneos_existentes = obtener_torneos()
                grid_torneos.controls.clear()
                for torneo in torneos_existentes:
                    grid_torneos.controls.append(crear_card_torneo(torneo))
                page.update()

                page.controls.remove(dlg)
                page.update()

            except Exception as err:
                print(f"Other error occurred: {err}")

        def cerrar_dialogo(e):
            page.controls.remove(dlg)
            page.update()

        dlg = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Editar Torneo", size=20, weight="bold"),
                    nombre_field,
                    categoria_field,
                    fecha_field,
                    hora_field,
                    ft.Row(
                        [
                            ft.ElevatedButton("Guardar", on_click=lambda e: guardar_torneo(e, id_edición), color=ft.Colors.BLUE_600),
                            ft.ElevatedButton("Cancelar", on_click=cerrar_dialogo, color=ft.Colors.RED_400),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=15,
                tight=True,
            ),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            width=400,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12),
        )

        page.controls.append(dlg)
        page.update()

    # Función para eliminar un torneo
    def eliminar_torneo(torneo):
        try:
            response = api_client.delete(f"eventos/{torneo['id']}")
            torneos_existentes = obtener_torneos()
            grid_torneos.controls.clear()
            for torneo in torneos_existentes:
                grid_torneos.controls.append(crear_card_torneo(torneo))
            page.update()
        except Exception as e:
            print(f"Error al eliminar el torneo: {e}")

    # Cargar los torneos desde la API
    torneos_existentes = obtener_torneos()

    # Barra de herramientas
    btn_volver = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: go_back(page)
    )

    search_field = ft.TextField(
        hint_text="Filtrar por nombre de torneo",
        width=300,
        color=ft.Colors.WHITE
    )

    btn_buscar = ft.ElevatedButton("Buscar", on_click=buscar_torneos)

    btn_crear_torneo = ft.ElevatedButton(
        "Crear torneo",
        on_click=mostrar_formulario_crear,
        color=ft.Colors.BLUE_600
    )


    toolbar_left = ft.Row(
        controls=[btn_volver, search_field, btn_buscar, btn_crear_torneo, btn_inicio],
        alignment=ft.MainAxisAlignment.START
    )

    toolbar = ft.Row(
        controls=[toolbar_left],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    grid_torneos = ft.GridView(
        expand=True,
        max_extent=250,
        runs_count=3,  # Cantidad de columnas en la cuadrícula
        spacing=10,
        run_spacing=10,
    )

    # Mostrar los torneos ya existentes en el grid
    for torneo in torneos_existentes:
        grid_torneos.controls.append(crear_card_torneo(torneo))

    main_container = ft.Column(
        controls=[toolbar, grid_torneos],
        spacing=10
    )

    visual_container = ft.Container(
        content=main_container,
        gradient=ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_200], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
        expand=True,
    )

    return visual_container


Gestionar_torneos = gestionar_torneos

__all__ = ["gestionar_torneos"]