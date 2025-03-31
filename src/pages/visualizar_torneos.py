import flet as ft
from models.event import Event
from models.event_type import Event_Type

def visualizar_torneos_view(page: ft.Page):
    # --- Creación de la barra de herramientas ---
    combo = ft.Dropdown(
        options=[
            ft.dropdown.Option("Opción 1"),
            ft.dropdown.Option("Opción 2"),
            ft.dropdown.Option("Opción 3"),
        ],
        hint_text="Seleccionar opción"
    )
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: page.on_back() if hasattr(page, "on_back") else None
    )
    btn_buscar = ft.ElevatedButton("Buscar", on_click=lambda e: print("Buscar"))

    toolbar_left = ft.Row(
        controls=[btn_volver, combo, btn_buscar],
        alignment=ft.MainAxisAlignment.START
    )
    toolbar = ft.Row(
        controls=[toolbar_left],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # --- Creación de la cuadrícula para torneos ---
    grid_torneos = ft.GridView(
        expand=True,
        max_extent=250,
        runs_count=3,  # Cantidad de columnas en la cuadrícula
        spacing=10,
        run_spacing=10,
    )

    # Contenedor principal que une la barra y la cuadrícula.
    main_container = ft.Column(
        controls=[toolbar, grid_torneos],
        spacing=10
    )

    # --- Función interna para crear la tarjeta de un torneo ---
    def crear_card_torneo(torneo: Event, torneo_info: Event_Type):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Nombre: {torneo.nombre}", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(f"Fecha: {torneo.fecha}"),
                        ft.Text(f"Hora: ${torneo.hora}"),
                        ft.Text(f"Podio: ${torneo_info.podio}"),
                    ],
                    spacing=5,
                ),
                padding=10,
                bgcolor=ft.Colors.BLACK,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            ),
            elevation=2,
            height=30
        )

    # --- Función interna para cargar torneos en la cuadrícula ---
    def cargar_torneos(torneos, event_types):
        grid_torneos.controls.clear()
        for event_type in event_types:
            if event_type.tipo == 1:
                for torneo in torneos:
                    if torneo.ID == event_type.eventoID:
                        grid_torneos.controls.append(crear_card_torneo(torneo, event_type))
        page.update()

    # Se adjunta la función de carga al contenedor para poder llamarla externamente.
    main_container.cargar_torneos = cargar_torneos

    return main_container


Visualizar_torneos = visualizar_torneos_view

__all__ = ["visualizar_torneos"]
