import flet as ft
from utils.api_client import api_client  # Asegúrate de que el cliente de la API esté disponible
import requests

def visualizar_entrenamientos(page: ft.Page):

    # Función para obtener los entrenamientos desde la API
    def obtener_torneos():
        try:
            # Realiza la solicitud GET para obtener los eventos
            response = api_client.get("eventos")  # Asumimos que la ruta es /eventos
            return response  # La respuesta será una lista de eventos
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los eventos: {e}")
            return []  # En caso de error, retornamos una lista vacía

    # Función para obtener el tipo de evento (incluyendo el profesor) desde la API
    def obtener_tipo_evento(tipo_id):
        try:
            # Realiza la solicitud GET para obtener el tipo de evento, pasando el tipo como parámetro
            response = api_client.get(f"eventosTipos/{tipo_id}")  # Ruta para obtener tipo de evento por ID
            return response  # Devuelve el tipo de evento, que incluirá el profesorID
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener tipo de evento: {e}")
            return None  # En caso de error, retornamos None

    # Cargar los eventos desde la API
    eventos = obtener_torneos()

    # Función para crear tarjeta de evento
    def crear_card_entrenamiento(evento):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(evento["nombre"], size=20, weight="bold"),
                        ft.Text(f"Fecha: {evento['fecha']}"),
                        ft.Text(f"Hora: {evento['hora']}"),
                        ft.Text(f"Profesor: {evento['profesor']}"),  # Mostramos el nombre del profesor
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

    # Filtro de búsqueda
    search_field = ft.TextField(hint_text="Filtrar por nombre de evento", width=300, color=ft.Colors.WHITE)

    # Función de búsqueda
    def buscar_entrenamientos(e):
        filtro = search_field.value.lower()
        filtered_entrenamientos = [evento for evento in eventos if filtro in evento["nombre"].lower()]
        
        # Limpiar y agregar tarjetas filtradas
        grid_entrenamientos.controls.clear()
        for entrenamiento in filtered_entrenamientos:
            grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))
        page.update()

    # Crear Grid de eventos
    grid_entrenamientos = ft.GridView(
        expand=True,
        max_extent=350,
        runs_count=2,  # Dos columnas
        spacing=10,
        run_spacing=10,
    )

    # Inicialmente se muestran todos los eventos
    for evento in eventos:
        # Asignamos el tipo de evento con ID 2
        evento["tipo"] = 2  # Aseguramos que el tipo de evento sea 2
        
        # Obtenemos el tipo de evento (incluyendo el profesor)
        tipo_evento = obtener_tipo_evento(evento["tipo"])
        
        if tipo_evento:
            # Suponemos que tipo_evento tiene el campo "profesorID", lo obtenemos
            profesor_id = tipo_evento.get("profesorID", "")
            
            # Asignamos el nombre del profesor si se encuentra en el tipo de evento
            evento["profesor"] = profesor_id.split(' ')[0]  # Extraemos el nombre del profesor, suponiendo el formato adecuado
            
            # Agregamos el evento con la información completa
            grid_entrenamientos.controls.append(crear_card_entrenamiento(evento))

    # Barra de herramientas
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: go_back(page)  # Llamamos a la función para regresar
    )

    btn_buscar = ft.ElevatedButton("Buscar", on_click=buscar_entrenamientos)

    btn_inicio = ft.ElevatedButton("Volver al inicio", on_click=lambda e: print("Volver al inicio"), color=ft.Colors.TEAL_600)

    toolbar_left = ft.Row(
        controls=[btn_volver, search_field, btn_buscar, btn_inicio],
        alignment=ft.MainAxisAlignment.START
    )

    toolbar = ft.Row(
        controls=[toolbar_left],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Contenedor principal
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

# Función para regresar al menú principal
def go_back(page):
    if hasattr(page, "on_back"):
        page.on_back()  # Llamamos a la función de regresar al menú
    else:
        page.clean()  # Limpiamos la página actual y volvemos a cargar el menú
        page.update()

Visualizar_entrenamientos = visualizar_entrenamientos

__all__ = ["Visualizar_entrenamientos"]
