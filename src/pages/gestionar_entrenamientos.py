import flet as ft
from models.event import Event, EventBuilder
from models.event_type import Event_Type, Event_TypeBuilder
import datetime
from utils.ConexionDB import api_client  # Asegúrate de tener la configuración correcta para api_client

def gestionar_entrenamientos(page: ft.Page):

    entrenamientos_simulados = []  # Lista donde almacenaremos los entrenamientos creados

    # Lista de profesores: La obtendremos de la API
    profesores = []

    # Función común para procesar los formularios (creación y edición)
    def procesar_entrenamiento(event_data, page, dlg, is_creacion=True):
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

            evento_data = {
                "nombre": event.nombre,
                "fecha": str(event.fecha),
                "hora": str(event.hora),
                "tipo": 2,  # Aseguramos que el tipo es 2
                "categoria": event_data['categoria'],
                "podio": 0  # Mandamos 0 explícitamente en el campo podio
            }

            if is_creacion:
                response_evento = api_client.post("eventos", evento_data)
            else:
                response_evento = api_client.put(f"eventos/{event_data['id']}", evento_data)

            evento_tipo_data = {
                "tipo": 2,  # Aseguramos que el tipo es 2
                "eventoID": event.ID,
                "profesorID": event_data['profesorID'],
                "podio": 0  # Mandamos 0 explícitamente en el campo podio
            }

            if is_creacion:
                response_evento_tipo = api_client.post("eventosTipos", evento_tipo_data)
            else:
                response_evento_tipo = api_client.put(f"eventosTipos/{event_data['tipo']}", evento_tipo_data)

            # Recargar los entrenamientos después de la creación o edición
            entrenamientos_existentes = obtener_entrenamientos()
            grid_entrenamientos.controls.clear()
            for entrenamiento in entrenamientos_existentes:
                grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))

            page.controls.remove(dlg)
            page.update()

        except ValueError as ex:
            print("Error en formato de fecha u hora:", ex)

    # Función para crear tarjeta de entrenamiento
    def crear_card_entrenamiento(entrenamiento):
        # Verificar si el campo 'profesorID' existe en el entrenamiento
        profesor_id = entrenamiento.get('profesorID')

        if profesor_id:
            # Buscar el nombre del profesor usando el profesorID
            profesor = next((profesor['nombre'] for profesor in profesores if profesor['id'] == profesor_id), "Desconocido")
        else:
            profesor = "Desconocido"

        # Crear los botones de Modificar y Eliminar
        btn_modificar = ft.ElevatedButton("Modificar", on_click=lambda e: mostrar_formulario_editar(entrenamiento), color=ft.Colors.YELLOW_600)
        btn_eliminar = ft.ElevatedButton("Eliminar", on_click=lambda e: eliminar_entrenamiento(entrenamiento), color=ft.Colors.RED_600)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(entrenamiento["nombre"], size=20, weight="bold"),
                        ft.Text(f"Fecha: {entrenamiento['fecha']}"),
                        ft.Text(f"Hora: {entrenamiento['hora']}"),
                        ft.Text(f"Categoria: {evento['categoria']}"),  # Mostramos la categoría
                        ft.Text(f"Profesor: {profesor}"),
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

    # Función para obtener la lista de profesores desde la API
    def obtener_profesores():
        try:
            response = api_client.get("personas")  # Asumimos que la ruta es /personas
            profesores = [persona for persona in response if persona['rol'] == 'Profesor']
            return profesores
        except Exception as e:
            print(f"Error al obtener los profesores: {e}")
            return []

    # Función para obtener los entrenamientos existentes desde la API
    def obtener_entrenamientos():
        try:
            response = api_client.get("eventos")  # La ruta sigue siendo /eventos
            # Filtrar solo los entrenamientos cuyo tipo sea 2
            entrenamientos_tipo_2 = [evento for evento in response if evento.get('tipo') == 2]
            return entrenamientos_tipo_2
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
    def buscar_entrenamientos(e):
        filtro = search_field.value.lower()
        
        filtered_entrenamientos = [entrenamiento for entrenamiento in entrenamientos_existentes if filtro in entrenamiento["nombre"].lower()]

        # Limpiar y agregar tarjetas filtradas
        grid_entrenamientos.controls.clear()
        for entrenamiento in filtered_entrenamientos:
            grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))
        page.update()

    # Función para obtener el ID del profesor basado en su nombre
    def obtener_profesor_id(nombre_profesor):
        for profesor in profesores:
            if profesor['nombre'] == nombre_profesor:
                return profesor['id']
        return None  # Si no se encuentra al profesor

    # Función para crear un nuevo entrenamiento
    def mostrar_formulario_crear(e):
        nombre_field = ft.TextField(label="Nombre del entrenamiento", hint_text="Nombre del entrenamiento")
        categoria_field =  ft.Dropdown(
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
        fecha_field = ft.TextField(label="Fecha del entrenamiento", hint_text="aaaa-mm-dd")
        hora_field = ft.TextField(label="Hora del entrenamiento", hint_text="hh:mm")

        profesor_field = ft.Dropdown(
            label="Selecciona el nombre del profesor",
            options=[ft.dropdown.Option(profesor['nombre']) for profesor in profesores],
            width=300,
        )

        def guardar_entrenamiento(e):
            profesor_id = obtener_profesor_id(profesor_field.value)
            if not profesor_id:
                print("Profesor no encontrado.")
                return

            # Solo enviar el ID del profesor y los datos esenciales
            event_data = {
                'nombre': nombre_field.value,
                'categoria': categoria_field.value,
                'fecha': fecha_field.value,
                'hora': hora_field.value,
                'tipo': 2,  # Todos los entrenamientos son de tipo 2
                'profesorID': profesor_id,  # Solo el ID del profesor
                'podio': 0  # Enviamos el valor 0 en el campo podio
            }

            # Llamar a la API para crear el evento
            try:
                response_evento = api_client.post("eventos", event_data)
                print("Respuesta de la API:", response_evento)

                entrenamientos_existentes = obtener_entrenamientos()
                grid_entrenamientos.controls.clear()
                for entrenamiento in entrenamientos_existentes:
                    grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))
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
                    ft.Text("Crear Entrenamiento", size=20, weight="bold"),
                    nombre_field,
                    categoria_field,
                    fecha_field,
                    hora_field,
                    profesor_field,
                    ft.Row(
                        [
                            ft.ElevatedButton("Guardar", on_click=guardar_entrenamiento, color=ft.Colors.BLUE_600),
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

    # Función para modificar un entrenamiento
    def mostrar_formulario_editar(entrenamiento):
        nombre_field = ft.TextField(label="Nombre del entrenamiento", hint_text="Ingresa el nombre", value=entrenamiento["nombre"])
        categoria_field = categoria_field =  ft.Dropdown(
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
        fecha_field = ft.TextField(label="Fecha del entrenamiento", hint_text="aaaa-mm-dd", value=entrenamiento["fecha"])
        hora_field = ft.TextField(label="Hora del entrenamiento", hint_text="hh:mm", value=entrenamiento["hora"])

        print("Entrenamiento a editar:", entrenamiento)
        id_edición = entrenamiento["id"]
        print("ID de edición:", id_edición)
        profesor_field = ft.Dropdown(
            label="Selecciona el nombre del profesor",
            options=[ft.dropdown.Option(profesor['nombre']) for profesor in profesores],
            value=entrenamiento.get("profesor", ""),
            width=300,
        )

        def guardar_entrenamiento(e, id_edicion, entrenamiento):    
            profesor_id = obtener_profesor_id(profesor_field.value)
            idedit = id_edicion
            # Ahora 'entrenamiento' está disponible aquí
            print("Entrenamiento a editar:", entrenamiento)
            
            event_data = {
                'id': id_edición,  # El ID del entrenamiento que se está editando
                'nombre': nombre_field.value,
                'categoria': categoria_field.value,
                'fecha': fecha_field.value,
                'hora': hora_field.value,
                'tipo': 2,  # Todos los entrenamientos son de tipo 2
                'profesorID': profesor_id,  # Solo el ID del profesor
                'podio': 0  # Enviamos el valor 0 en el campo podio
            }

            # Llamar a la API para actualizar el evento
            try:
                response_evento = api_client.put(f"eventos/{entrenamiento['id']}", event_data)
                print("Respuesta de la API:", response_evento)

                entrenamientos_existentes = obtener_entrenamientos()
                grid_entrenamientos.controls.clear()
                for entrenamiento in entrenamientos_existentes:
                    grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))
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
                    ft.Text("Editar Entrenamiento", size=20, weight="bold"),
                    nombre_field,
                    categoria_field,
                    fecha_field,
                    hora_field,
                    profesor_field,
                    ft.Row(
                        [
                            ft.ElevatedButton("Guardar", on_click=lambda e: guardar_entrenamiento(e, id_edición, entrenamiento), color=ft.Colors.BLUE_600),
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

    # Función para eliminar un entrenamiento
    def eliminar_entrenamiento(entrenamiento):
        try:
            response = api_client.delete(f"eventos/{entrenamiento['id']}")
            entrenamientos_existentes = obtener_entrenamientos()
            grid_entrenamientos.controls.clear()
            for evento in entrenamientos_existentes:
                grid_entrenamientos.controls.append(crear_card_entrenamiento(evento))
            page.update()
        except Exception as e:
            print(f"Error al eliminar el evento: {e}")

    # Cargar los profesores desde la API
    profesores = obtener_profesores()

    # Cargar los eventos ya existentes desde la API
    entrenamientos_existentes = obtener_entrenamientos()

    # Barra de herramientas
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: go_back(page)
    )

    search_field = ft.TextField(
    hint_text="Filtrar por nombre de entrenamiento",
    width=300,
    color=ft.Colors.BLACK,  # color del texto ingresado
    hint_style=ft.TextStyle(color=ft.Colors.BLACK54),  # color del placeholder
)

    btn_buscar = ft.ElevatedButton("Buscar", on_click=buscar_entrenamientos)

    btn_crear_entrenamiento = ft.ElevatedButton(
        "Crear entrenamiento",
        on_click=mostrar_formulario_crear,
        color=ft.Colors.BLUE_600
    )

    toolbar_left = ft.Row(
        controls=[btn_volver, search_field, btn_buscar, btn_crear_entrenamiento],
        alignment=ft.MainAxisAlignment.START
    )

    toolbar = ft.Row(
        controls=[toolbar_left],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    grid_entrenamientos = ft.GridView(
        expand=True,
        max_extent=250,
        runs_count=3,
        spacing=10,
        run_spacing=10,
    )

    # Mostrar los entrenamientos ya existentes en el grid
    for evento in entrenamientos_existentes:
        grid_entrenamientos.controls.append(crear_card_entrenamiento(evento))

    main_container = ft.Column(
        controls=[toolbar, grid_entrenamientos],
        spacing=10
    )

    visual_container = ft.Container(
        content=main_container,
        gradient=ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_200], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
        expand=True,
    )

    return visual_container


Gestionar_entrenamientos = gestionar_entrenamientos

__all__ = ["gestionar_entrenamientos"]