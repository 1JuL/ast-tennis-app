import flet as ft
from models.event import Event, EventBuilder
from models.event_type import Event_Type, Event_TypeBuilder
import datetime
from utils.api_client import api_client

def gestionar_entrenamientos(page: ft.Page):

    entrenamientos_simulados = []  # Lista donde almacenaremos los entrenamientos creados

    # Lista de profesores: La obtendremos de la API
    profesores = []

    # Función para crear tarjeta de entrenamiento
    def crear_card_entrenamiento(entrenamiento):
        # Asegurarse de que 'profesor' esté en el evento, si no, asignamos un valor por defecto
        profesor = entrenamiento.get("profesor", "Desconocido")
        
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
                        ft.Text(f"Profesor: {profesor}"),  # Mostramos el nombre del profesor
                        ft.Row([btn_modificar, btn_eliminar], spacing=10, alignment=ft.MainAxisAlignment.CENTER)  # Botones debajo
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
            # Realiza la solicitud GET para obtener las personas
            response = api_client.get("personas")  # Asumimos que la ruta es /personas
            # Filtrar solo aquellos con el rol 'Profesor'
            profesores = [persona for persona in response if persona['rol'] == 'Profesor']
            return profesores  # La respuesta será una lista de profesores
        except Exception as e:
            print(f"Error al obtener los profesores: {e}")
            return []  # En caso de error, retornamos una lista vacía

    # Función para obtener los entrenamientos existentes desde la API
    def obtener_entrenamientos():
        try:
            # Realiza la solicitud GET para obtener los eventos
            response = api_client.get("eventos")  # Asumimos que la ruta es /eventos
            return response  # La respuesta será una lista de eventos
        except Exception as e:
            print(f"Error al obtener los eventos: {e}")
            return []  # En caso de error, retornamos una lista vacía

    # Función para volver al menú o la vista anterior
    def go_back(page):
        if hasattr(page, "on_back"):
            page.on_back()  # Llamamos a la función de regresar al menú
        else:
            page.clean()  # Limpiamos la página actual y volvemos a cargar el menú
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

    # Función para modificar un entrenamiento: carga el formulario con los datos actuales
    def mostrar_formulario_editar(entrenamiento):
        # Definir los campos del formulario de edición
        nombre_field = ft.TextField(label="Nombre del entrenamiento", hint_text="Ingresa el nombre", value=entrenamiento["nombre"])
        categoria_field = ft.TextField(label="Categoría", hint_text="Ingresa la categoría", value=entrenamiento["categoria"])
        fecha_field = ft.TextField(label="Fecha del entrenamiento", hint_text="dd/mm/aaaa", value=entrenamiento["fecha"])
        hora_field = ft.TextField(label="Hora del entrenamiento", hint_text="hh:mm", value=entrenamiento["hora"])

        # Aquí, profesor_field es un dropdown que carga los profesores disponibles
        profesor_field = ft.Dropdown(
            label="Selecciona el nombre del profesor",
            options=[ft.dropdown.Option(profesor['nombre']) for profesor in profesores],
            value=entrenamiento.get("profesor", ""),  # Asignamos el valor del profesor actual
            width=300,
        )

        # Ahora, con los valores precargados, podemos actualizar el formulario
        page.update()

        # Función para guardar los cambios en el entrenamiento
        def guardar_entrenamiento(e, entrenamiento):  # Se pasa 'entrenamiento' como parámetro
            try:
                # Convertir la fecha y hora a formato de fecha y hora
                fecha = datetime.datetime.strptime(fecha_field.value, '%d/%m/%Y').date()
                hora = datetime.datetime.strptime(hora_field.value, '%H:%M').time()

                # Crear un nuevo evento usando el EventBuilder
                event = EventBuilder()\
                    .set_nombre(nombre_field.value)\
                    .set_fecha(fecha)\
                    .set_hora(hora)\
                    .set_tipo(categoria_field.value)\
                    .build()

                # Preparar los datos para enviar a la API
                evento_data = {
                    "nombre": event.nombre,
                    "fecha": str(event.fecha),
                    "hora": str(event.hora),
                    "tipo": 2,  # Aseguramos que el tipo es 2
                    "categoria": categoria_field.value
                }

                # Llamar a la API para actualizar el evento
                response_evento = api_client.put(f"eventos/{entrenamiento['id']}", evento_data)

                # Crear o actualizar el tipo de evento con el ID del profesor
                evento_tipo_data = {
                    "tipo": 2,  # Aseguramos que el tipo es 2
                    "eventoID": event.ID,
                    "profesorID": profesor_field.value,  # Usamos el valor del dropdown para obtener el ID del profesor
                    "podio": "1er lugar"
                }

                response_evento_tipo = api_client.put(f"eventosTipos/{entrenamiento['tipo']}", evento_tipo_data)

                print("Evento actualizado:", response_evento)
                print("Tipo de evento actualizado:", response_evento_tipo)

                # Cargar los eventos ya existentes nuevamente para mantener la lista completa
                entrenamientos_existentes = obtener_entrenamientos()

                # Limpiar y agregar las tarjetas de todos los entrenamientos (existentes + nuevos)
                grid_entrenamientos.controls.clear()
                for entrenamiento in entrenamientos_existentes:
                    grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))

                page.controls.remove(dlg)
                page.update()

            except ValueError as ex:
                print("Error en formato de fecha u hora:", ex)

        def cerrar_dialogo(e):
            page.controls.remove(dlg)
            page.update()

        # Crear el cuadro de diálogo para la edición
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
                            ft.ElevatedButton("Guardar", on_click=lambda e: guardar_entrenamiento(e, entrenamiento), color=ft.Colors.BLUE_600),
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

    # Función para eliminar un entrenamiento
    def eliminar_entrenamiento(entrenamiento):
        print(f"Eliminando el entrenamiento: {entrenamiento['nombre']}")
        try:
            # Llamar a la API para eliminar el evento usando su ID
            response = api_client.delete(f"eventos/{entrenamiento['id']}")  # Asumiendo que 'id' es el identificador del evento
            if response:
                print("Evento eliminado exitosamente.")
                # Recargar los eventos después de eliminar
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
        on_click=lambda e: go_back(page)  # Llamamos a la función para regresar
    )

    # Campo de texto para buscar entrenamientos
    search_field = ft.TextField(
        hint_text="Filtrar por nombre de entrenamiento", 
        width=300, 
        color=ft.Colors.WHITE
    )

    btn_buscar = ft.ElevatedButton("Buscar", on_click=buscar_entrenamientos)

    btn_crear_entrenamiento = ft.ElevatedButton(
        "Crear entrenamiento",
        on_click=mostrar_formulario_editar,  # Cambié a mostrar_formulario_editar en vez de mostrar_crear_entrenamiento
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

    # Mostrar los entrenamientos ya existentes en el grid
    for evento in entrenamientos_existentes:
        grid_entrenamientos.controls.append(crear_card_entrenamiento(evento))

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
