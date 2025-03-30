import flet as ft
from models.event import Event, EventBuilder
from models.event_type import Event_Type, Event_TypeBuilder
import datetime
from utils.api_client import api_client  # Asegúrate de que el cliente de la API esté disponible

def gestionar_entrenamientos(page: ft.Page):

    entrenamientos_simulados = []  # Lista donde almacenaremos los entrenamientos creados

    # Función para crear tarjeta de entrenamiento
    def crear_card_entrenamiento(entrenamiento):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(entrenamiento["nombre"], size=20, weight="bold"),
                        ft.Text(f"Fecha: {entrenamiento['fecha']}"),
                        ft.Row(
                            [
                                ft.ElevatedButton("Actualizar", color=ft.Colors.YELLOW_600),
                                ft.ElevatedButton("Borrar", color=ft.Colors.RED_600)
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.END
                        )
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

    # Función para obtener los profesores de la API
    def obtener_profesores():
        profesores = []
        try:
            # Realizar la solicitud GET a la API para obtener todas las personas
            response = api_client.get("personas")
            personas = response  # No es necesario llamar a .json() si ya es una lista
            
            # Filtrar las personas por categoría "Profesor"
            profesores = [f"{persona['nombre']} {persona['apellido']} ({persona['uid']})" 
                          for persona in personas if persona['categoria'] == 'Profesor']

            return profesores
        except Exception as e:
            print("Error al obtener profesores:", e)
            return []

    # Función para mostrar el diálogo de crear entrenamiento
    def mostrar_crear_entrenamiento(e):
        nombre_field = ft.TextField(label="Nombre del entrenamiento", hint_text="Ingresa el nombre")
        categoria_field = ft.TextField(label="Categoría", hint_text="Ingresa la categoría")

        # Fecha con TextField, ahora solo texto
        fecha_field = ft.TextField(
            label="Fecha del entrenamiento",
            hint_text="dd/mm/aaaa"
        )

        # Hora con TextField, ahora solo texto
        hora_field = ft.TextField(
            label="Hora del entrenamiento",
            hint_text="hh:mm"
        )

        # Obtener los profesores de la API
        profesores = obtener_profesores()

        # ScrollBox con los nombres de los profesores
        profesor_field = ft.Dropdown(
            label="Selecciona el nombre del profesor",
            options=[ft.dropdown.Option(profesor) for profesor in profesores],
            width=300,
        )

        def guardar_entrenamiento(e):
            try:
                # Convertir la fecha y hora a formato de fecha y hora
                fecha = datetime.datetime.strptime(fecha_field.value, '%d/%m/%Y').date()
                hora = datetime.datetime.strptime(hora_field.value, '%H:%M').time()

                # Crear un nuevo evento usando el EventBuilder
                event = EventBuilder()\
                    .set_nombre(nombre_field.value)\
                    .set_fecha(fecha)\
                    .set_hora(hora)\
                    .set_tipo(2)\
                    .build()

                # Crear el tipo de evento asociado con tipo de evento ID 2 (como especificaste)
                event_type = Event_TypeBuilder()\
                    .set_tipo(categoria_field.value)\
                    .set_eventoID(event.ID)\
                    .set_profesorID(profesor_field.value)\
                    .set_podio("1er lugar").build()

                # Asignar el tipo de evento con ID 2
                event_type.tipo = 2  # Aquí asignamos el tipo de evento con ID 2

                # Preparar los datos para enviar a la API
                evento_data = {
                    "nombre": event.nombre,
                    "fecha": str(event.fecha),
                    "hora": str(event.hora),
                    "tipo": 2,
                    "categoria": categoria_field.value
                }

                evento_tipo_data = {
                    "tipo": 2,  # El tipo de evento es ahora 2
                    "eventoID": event_type.eventoID,
                    "profesorID": event_type.profesorID,
                    "podio": event_type.podio
                }

                # Llamar a la API para crear el evento y el tipo de evento
                response_evento = api_client.post("eventos", evento_data)
                response_evento_tipo = api_client.post("eventosTipos", evento_tipo_data)

                print("Evento creado:", response_evento)
                print("Tipo de evento creado:", response_evento_tipo)

                # Almacenar el nuevo entrenamiento en la lista de entrenamientos
                entrenamientos_simulados.append({
                    "nombre": event.nombre,
                    "fecha": str(event.fecha),
                })

                # Limpiar y agregar las tarjetas del nuevo entrenamiento
                grid_entrenamientos.controls.clear()
                for entrenamiento in entrenamientos_simulados:
                    grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))

                page.controls.remove(dlg)
                page.update()

            except ValueError as ex:
                print("Error en formato de fecha u hora:", ex)

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
                spacing=15,  # Ajustar el espaciado entre los elementos del formulario
                tight=True,
            ),
            padding=30,  # Más padding alrededor del cuadro de diálogo
            bgcolor=ft.Colors.WHITE,
            width=400,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12),
        )

        page.controls.append(dlg)
        page.update()

    # Barra de herramientas
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
    )

    # Campo de texto para buscar entrenamientos
    search_field = ft.TextField(
        hint_text="Filtrar por nombre de entrenamiento", 
        width=300, 
        color=ft.Colors.WHITE
    )

    btn_buscar = ft.ElevatedButton("Buscar", on_click=lambda e: print("Buscar"))

    btn_crear_entrenamiento = ft.ElevatedButton(
        "Crear entrenamiento",
        on_click=mostrar_crear_entrenamiento,
        color=ft.Colors.BLUE_600
    )

    btn_inicio = ft.ElevatedButton("Volver al inicio", on_click=lambda e: print("Volver al inicio"), color=ft.Colors.TEAL_600)

    toolbar_left = ft.Row(
        controls=[btn_volver, search_field, btn_buscar, btn_crear_entrenamiento, btn_inicio],
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

    # Mostrar los entrenamientos en el grid
    for entrenamiento in entrenamientos_simulados:
        grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))

    main_container = ft.Column(
        controls=[toolbar, grid_entrenamientos],
        spacing=10
    )

    # Contenedor con el estilo visual similar al de login (gradiente)
    visual_container = ft.Container(
        content=main_container,
        gradient=ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_200], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
        expand=True,
    )

    return visual_container


Gestionar_entrenamientos = gestionar_entrenamientos

__all__ = ["gestionar_entrenamientos"]
