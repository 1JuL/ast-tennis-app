import flet as ft

def visualizar_entrenamientos_view(page: ft.Page):

    dlg = ft.Container(
        padding=20,
        bgcolor=ft.Colors.WHITE,
        width=400,
        border_radius=8,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
    )

    page.controls.append(dlg)
    page.update()

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
    )

    btn_buscar = ft.ElevatedButton("Buscar", on_click=lambda e: print("Buscar"))

    btn_inicio = ft.ElevatedButton("Volver al inicio", on_click=lambda e: print("Volver al inicio"), color=ft.Colors.TEAL_600)

    toolbar_left = ft.Row(
        controls=[btn_volver, combo, btn_buscar, btn_inicio],  # Aquí se eliminó btn_crear_entrenamiento
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

    main_container = ft.Column(
        controls=[toolbar, grid_entrenamientos],
        spacing=10
    )

    return main_container


Visualizar_entrenamientos = visualizar_entrenamientos_view

__all__ = ["Visualizar_entrenamientos"]
