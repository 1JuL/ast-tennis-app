import flet as ft
from models.event import Event, EventBuilder
from models.event_type import Event_Type, Event_TypeBuilder
from utils.ConexionDB import api_client
from datetime import datetime


def gestionar_torneos_view(page: ft.Page):


    nombre_field = ft.TextField(label="Nombre del torneo", hint_text="Ingresa el nombre del torneo")
    fecha_field = ft.TextField(label="Fecha del torneo", hint_text="dd/mm/aaaa")
    hora_field = ft.TextField(label="Hora del torneo", hint_text="hh:mm")
    profesor_id_field = ft.TextField(label="Profesor anfitrión", hint_text="Ingresa el ID del profesor")
    primer_lugar_field = ft.TextField(label="Primer lugar", hint_text="Ingresa el ID del alumno")
    segundo_lugar_field = ft.TextField(label="Segundo lugar", hint_text="Ingresa el ID del alumno")
    tercer_lugar_field = ft.TextField(label="Tercer lugar", hint_text="Ingresa el ID del alumno")

    def crear_card_torneo(evento: Event):
        """ retorna la tarjeta de un pago """
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"ID: {evento.ID}", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, selectable=True),
                        ft.Text(f"Nombre: {evento.nombre}", selectable=True, color=ft.Colors.BLACK),
                        ft.Text(f"Fecha: {evento.fecha}", color=ft.Colors.BLACK),
                        ft.Text(f"Hora: {evento.hora}", color=ft.Colors.BLACK),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.PopupMenuButton(
                                    icon=ft.icons.MORE_VERT,
                                    items=[
                                        ft.PopupMenuItem(
                                            text="Eliminar",
                                            icon=ft.Icons.DELETE,
                                            on_click= lambda _: eliminarTorneo(evento.ID)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Modificar",
                                            icon=ft.Icons.EDIT_ROUNDED,
                                            on_click= lambda _: modificarTorneo(evento)
                                        )
                                    ],
                                )
                            ]
                        )
                    ],
                    spacing=5,
                ),
                padding=10,
                bgcolor=ft.Colors.GREY_50,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            ),
            elevation=2,
            height=30
        )


    def buscarTorneo():
        pass


    def eliminarTorneo(id):
        pass

    def modificarTorneo(torneo):
        nombre_field.value = torneo.nombre
        fecha_field.value = torneo.fecha
        hora_field.value = torneo.hora
        profesor_id_field.value = torneo.profesor_id

        page.open(dlg)

    def registrarTorneo():
        try:
            fecha = datetime.strptime(fecha_field.value, '%d/%m/%Y').date()
            hora = datetime.strptime(hora_field.value, '%H:%M').time()

            event = EventBuilder()\
                .set_nombre(nombre_field.value)\
                .set_fecha(fecha)\
                .set_hora(hora)\
                .set_tipo(1)\
                .build()
            
            event_type = Event_TypeBuilder()\
                .set_tipo(1)\
                .set_eventoID(event.ID)\
                .set_profesorID(profesor_id_field.value)\
                .set_podio([primer_lugar_field.value, segundo_lugar_field.value, tercer_lugar_field.value])\
                .build()
            
            print("Evento creado:", event.__dict__)
            print("Tipo de evento creado:", event_type.__dict__)

        except ValueError as ex:
            print("Error en formato de fecha u hora:", ex)

    dlg = ft.AlertDialog(
        modal=True,  # Hace que sea una ventana modal
        title=ft.Text("Registrar Torneo", size=20, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                nombre_field,
                fecha_field,
                hora_field,
                profesor_id_field,
                primer_lugar_field,
                segundo_lugar_field,
                tercer_lugar_field,
            ],
            tight=True,            # Ajusta el espacio vertical
            horizontal_alignment=ft.CrossAxisAlignment.START
        ),
        actions_alignment="end",  # Alinea los botones a la derecha
        actions=[
            ft.TextButton(
                "Cancelar", 
                on_click=lambda _: (
                    page.close(dlg)
                )
            ),
            ft.TextButton(
                "Registrar Torneo",
                on_click=lambda _: registrarTorneo()
            ),
        ],
    )

    
    def handle_change(e: ft.ControlEvent):
        if e.data is not None:  # Si se seleccionó una fecha
            fecha_input.value = e.control.value.strftime('%Y-%m-%d')
            page.update()

    def open_date_picker(e):
        page.open(ft.DatePicker(
                    on_change=handle_change,
                ))



    btn_volver = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: page.on_back() if hasattr(page, "on_back") else None
    )

    btn_crear_Torneo = ft.TextButton("Crear torneo", bgcolor=ft.Colors.WHITE, color=ft.Colors.RED_900, on_click=registrarTorneo())

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Buscar torneos...",
        view_hint_text="Escriba el nombre del torneo",
        on_submit=buscarTorneo()
    )

    toolbar = ft.Container(
    height=50,  # Ajusta la altura de la barra
    padding=ft.padding.symmetric(horizontal=15,vertical=5),  # Añade margen lateral
    content=ft.Row(
        controls=[
            ft.Row([btn_volver, btn_crear_Torneo], alignment=ft.MainAxisAlignment.START),
            anchor
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    ),
    bgcolor=ft.Colors.WHITE  # Fondo opcional para resaltar la barra
)

    

    grid_pagos = ft.GridView(
        expand=True,
        max_extent=250,
        runs_count=3,  # Cantidad de columnas en la cuadrícula
        spacing=10,
        run_spacing=10,
    )

    fecha_input = ft.TextField(
        label="Fecha de Pago",
        hint_text="aaaa-mm-dd",
        read_only=True,
        width=300,
        on_click= open_date_picker
                
    )


    # Construcción del contenedor principal que une la barra de herramientas y el grid
    main_container = ft.Container(
        content=ft.Column(
        controls=[toolbar, grid_pagos],
        spacing=10,
        expand= True, 
        ),
        gradient= ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_200], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
        expand=True,
    )
    return main_container

# Exportamos la función con el alias 'Gestionar_pagos'
Gestionar_torneos = gestionar_torneos_view

__all__ = ["gestionar_pagos"]
