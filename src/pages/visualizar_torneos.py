import flet as ft
from utils.ConexionDB import api_client  # Asegúrate de tener la configuración correcta para api_client

def visualizar_torneos_view(page: ft.Page):
    entrenamientos_simulados = []  # Lista donde almacenaremos los entrenamientos filtrados (tipo == 2)

    # Función para crear tarjeta de entrenamiento
    def crear_card_entrenamiento(entrenamiento):
        # Obtener el profesor ID del entrenamiento
        profesor_id = entrenamiento.get('profesorID')

        # Buscar el nombre del profesor usando el profesorID
        profesor = "Desconocido"
        if profesor_id:
            # Buscar el profesor en la lista de personas usando su ID
            profesor = obtener_nombre_profesor_por_id(profesor_id)

        # Crear los botones de Modificar y Eliminar
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(entrenamiento["nombre"], size=20, weight="bold"),
                        ft.Text(f"Fecha: {entrenamiento['fecha']}"),
                        ft.Text(f"Hora: {entrenamiento['hora']}"),
                        
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

    # Función para obtener el nombre del profesor usando el profesorID
    def obtener_nombre_profesor_por_id(profesor_id):
        try:
            response = api_client.get(f"personas/{profesor_id}")  # Obtener profesor por su ID desde la API
            if response:
                return response.get('nombre', 'Desconocido')
            return "Desconocido"
        except Exception as e:
            print(f"Error al obtener el profesor: {e}")
            return "Desconocido"

    # Función para obtener los entrenamientos con tipo == 2
    def obtener_entrenamientos_tipo_2():
        try:
            response = api_client.get("eventos")  # Asumimos que la ruta es /eventos
            entrenamientos = [entrenamiento for entrenamiento in response if entrenamiento['tipo'] == 1]
            return entrenamientos
        except Exception as e:
            print(f"Error al obtener los eventos: {e}")
            return []
    
    def go_back(page):
        if hasattr(page, "on_back"):
            page.on_back()
        else:
            page.clean()
            page.update()

    # Función para cargar los entrenamientos
    entrenamientos_existentes = obtener_entrenamientos_tipo_2()

    # Crear las tarjetas con los entrenamientos tipo 2
    grid_entrenamientos = ft.GridView(
        expand=True,
        max_extent=250,
        runs_count=3,
        spacing=10,
        run_spacing=10,
    )

    for entrenamiento in entrenamientos_existentes:
        grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))

    # Función de búsqueda
    def buscar_entrenamientos(e):
        filtro = search_field.value.lower()
        filtered_entrenamientos = [entrenamiento for entrenamiento in entrenamientos_existentes if filtro in entrenamiento["nombre"].lower()]

        # Limpiar y agregar tarjetas filtradas
        grid_entrenamientos.controls.clear()
        for entrenamiento in filtered_entrenamientos:
            grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))
        page.update()

    # Barra de herramientas
    btn_volver = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: go_back(page)
    )

    search_field = ft.TextField(
        hint_text="Filtrar por nombre de entrenamiento",
        width=300,
        color=ft.Colors.WHITE
    )

    btn_buscar = ft.ElevatedButton("Buscar", on_click=buscar_entrenamientos)

    toolbar_left = ft.Row(
        controls=[btn_volver, search_field, btn_buscar],
        alignment=ft.MainAxisAlignment.START
    )

    toolbar = ft.Row(
        controls=[toolbar_left],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

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



Visualizar_torneos = visualizar_torneos_view

__all__ = ["visualizar_torneos"]