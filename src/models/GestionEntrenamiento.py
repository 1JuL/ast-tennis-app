import flet as ft
from models.event import Event, EventBuilder
from models.event_type import Event_Type, Event_TypeBuilder
import datetime, time

def GestionEntrenamiento(page: ft.Page):

    def mostrar_crear_entrenamiento(e):
        nombre_field = ft.TextField(label="Nombre del entrenamiento", hint_text="Ingresa el nombre")
        fecha_field = ft.TextField(label="Fecha del entrenamiento", hint_text="dd/mm/aaaa")
        hora_field = ft.TextField(label="Hora del entrenamiento", hint_text="hh:mm")
        categoria_field = ft.TextField(label="Categoría", hint_text="Ingresa la categoría")
        profesor_id_field = ft.TextField(label="Profesor ID", hint_text="Ingresa el ID del profesor")

        def guardar_entrenamiento(e):
            try:
                # Convertir fecha y hora a objetos datetime y time
                fecha = datetime.datetime.strptime(fecha_field.value, '%d/%m/%Y').date()
                hora = datetime.datetime.strptime(hora_field.value, '%H:%M').time()

                # Construir evento usando EventBuilder
                event = EventBuilder()\
                    .set_nombre(nombre_field.value)\
                    .set_fecha(fecha)\
                    .set_hora(hora)\
                    .set_tipo(categoria_field.value)\
                    .build()

                # Aquí podrías generar o asignar un ID real
                event.ID = 1  # Ejemplo estático, deberías usar lógica real

                # Construir Event_Type usando Event_TypeBuilder
                event_type = Event_TypeBuilder()\
                    .set_tipo(categoria_field.value)\
                    .set_eventoID(event.ID)\
                    .set_profesorID(profesor_id_field.value)\
                    .build()

                # Aquí puedes agregar lógica para persistir estos objetos
                print("Evento creado:", event.__dict__)
                print("Tipo de evento creado:", event_type.__dict__)

                dlg.open = False
                page.update()
            except ValueError as ex:
                print("Error en formato de fecha u hora:", ex)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Crear Entrenamiento"),
            content=ft.Container(
                content=ft.Column(
                    [
                        nombre_field,
                        fecha_field,
                        hora_field,
                        categoria_field,
                        profesor_id_field,
                    ],
                    spacing=10,
                    tight=True,
                ),
                padding=20,
                width=400
            ),
            actions=[
                ft.ElevatedButton("Guardar Entrenamiento", on_click=guardar_entrenamiento, color=ft.Colors.BLUE_600),
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, 'open', False) or page.update())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dlg
        dlg.open = True
        page.update()

    # Barra de herramientas
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

    btn_crear_entrenamiento = ft.ElevatedButton(
        "Crear entrenamiento",
        on_click=mostrar_crear_entrenamiento,
        color=ft.Colors.BLUE_600
    )

    btn_inicio = ft.ElevatedButton(
        "Volver al inicio",
        on_click=lambda e: print("Volver al inicio"),
        color=ft.Colors.TEAL_600
    )

    toolbar_left = ft.Row(
        controls=[btn_volver, combo, btn_buscar, btn_crear_entrenamiento, btn_inicio],
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

__all__ = ["GestionEntrenamiento"]
