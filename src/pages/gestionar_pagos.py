import flet as ft
from models.Payment import Payment  # Ajusta la ruta según tu estructura de carpetas
from utils.ConexionDB import api_client

def gestionar_pagos_view(page: ft.Page):
    # Barra de herramientas
    combo = ft.Dropdown(
        options=[
        ],
        hint_text="Seleccione"
    )
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: page.on_back() if hasattr(page, "on_back") else None
    )
    btn_buscar = ft.ElevatedButton("Buscar", on_click=lambda e: print("Buscar"))
    btn_registrar = ft.ElevatedButton("Registrar pago", on_click=lambda e: print("Registrar pago"), color=ft.Colors.GREEN_500)
    btn_registrar_id = ft.ElevatedButton("Registrar pago por ID", on_click=lambda e: print("Registrar pago por ID"), color=ft.Colors.AMBER_500)

    toolbar_left = ft.Row(
        controls=[btn_volver, combo, btn_buscar],
        alignment=ft.MainAxisAlignment.START
    )
    toolbar_right = ft.Row(
        controls=[btn_registrar, btn_registrar_id],
        alignment=ft.MainAxisAlignment.END
    )
    toolbar = ft.Row(
        controls=[toolbar_left, toolbar_right],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    grid_pagos = ft.GridView(
        expand=True,
        max_extent=250,
        runs_count=3,  # Cantidad de columnas en la cuadrícula
        spacing=10,
        run_spacing=10,
    )


    # funcion para cargar los usuarios al combo box
    def cargarUsuariosCombo():
        """ se cargan los usuarios al combox box """
        pass

        


    # Función para crear la tarjeta de un pago
    def crear_card_pago(pago: Payment):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"ID: {pago.ID}", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(f"ID Persona: {pago.personaId}"),
                        ft.Text(f"Monto: ${pago.monto:.2f}"),
                        ft.Text(f"Fecha: {pago.fecha}"),
                        ft.Text(
                            f"Estado: {pago.estado}",
                            color=ft.Colors.AMBER_500 if pago.estado == 'Pendiente' else ft.Colors.GREEN_500
                        )
                    ],
                    spacing=5,
                ),
                padding=10,
                bgcolor=ft.Colors.SURFACE,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                border=ft.border.all(2, ft.Colors.AMBER_500 if pago.estado == 'Pendiente' else ft.Colors.GREEN_500),
            ),
            elevation=2,
            height=30
        )

    # Función para cargar pagos en el grid
    def cargar_pagos(pagos):
        grid_pagos.controls.clear()
        for pago in pagos:
            grid_pagos.controls.append(crear_card_pago(pago))

    # Construcción del contenedor principal que une la barra de herramientas y el grid
    main_container = ft.Column(
        controls=[toolbar, grid_pagos],
        spacing=10
    )

    # Simulación de carga de pagos (en la práctica recibirás una lista real)
    pagos_simulados = [
        Payment(1, 1, 28000, '28-10-2025'),
        Payment(1, 1, 30000, '28-10-2025', "Pagado")
    ]
    cargar_pagos(pagos_simulados)

    return main_container

# Exportamos la función con el alias 'Gestionar_pagos'
Gestionar_pagos = gestionar_pagos_view

__all__ = ["gestionar_pagos"]
