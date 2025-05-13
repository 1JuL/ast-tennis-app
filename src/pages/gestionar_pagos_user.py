import flet as ft
from models.Payment import Payment  # Ajusta la ruta según tu estructura de carpetas
from utils.ConexionDB import api_client
from utils.global_state import auth_state
from datetime import datetime
import asyncio  # al principio del archivo




def gestionar_pagos_user_view(page: ft.Page):

    async def getPagos():
        """Se piden los pagos de la persona mediante su id y se cargan en el gridView"""
        await asyncio.sleep(0.1)  # Espera a que la vista esté completamente cargada
        pagosUsuario = [] # en este arreglo se cargarán los objetos tipo Payment del usuario
        print('Consiguiendo id y pagos')
        dlg_aviso = ft.AlertDialog(
            modal=True,
            title=ft.Text("Aviso"),
            content=ft.Text("Al parecer no hay pagos a su nombre, por ahora..."),
            actions=[
                ft.TextButton("Aceptar", on_click=lambda _: page.close(dlg_aviso)),
            ],
            actions_alignment=ft.MainAxisAlignment.END)
        
        try:
            
            id = getId()
            pagos = api_client.get(f"pagos/usuario/{id}")
            print(pagos)
            for pago in pagos:
                pagosUsuario.append(Payment(pago["id"],pago["personalID"], float(pago["monto"]), datetime.strptime(pago['fecha'], '%Y-%m-%d') , pago["estado"]))

            print(pagosUsuario)
            cargar_pagos(pagosUsuario)
        except:
            page.open(dlg_aviso)
            grid_pagos.clean()
            grid_pagos.update()
            

    def getId():
        personas = api_client.get(f"personas/uid/{auth_state.user.get("localId")}")
        persona  = personas[0] if isinstance(personas, list) else personas
        id = persona.get("id")
        return id
    def crear_card_pago(pago: Payment):
        """ retorna la tarjeta de un pago """
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"ID: {pago.ID}", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, selectable=True),
                        ft.Text(f"ID Persona: {pago.personaId}", selectable=True, color=ft.Colors.BLACK),
                        ft.Text(f"Monto: ${pago.monto:.2f}", color=ft.Colors.BLACK),
                        ft.Text(f"Fecha: {pago.fecha}", color=ft.Colors.BLACK),
                        ft.Text(
                            f"Estado: {pago.estado}",
                            color=ft.Colors.AMBER_500 if pago.estado == 'Pendiente' else ft.Colors.GREEN_500,
                        ),
                    ],
                    spacing=5,
                ),
                padding=10,
                bgcolor=ft.Colors.GREY_50,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                border=ft.border.all(2, ft.Colors.AMBER_500 if pago.estado == 'Pendiente' else ft.Colors.GREEN_500),
            ),
            elevation=2,
            height=30
        )

    def cargar_pagos(pagos):
        """carga los pagos en el grid"""
        grid_pagos.controls.clear()
        for pago in pagos:
            grid_pagos.controls.append(crear_card_pago(pago))
        grid_pagos.update()

    # Barra de herramientas
    

    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: page.go("/user_menu"),
    )
    toolbar_left = ft.Row(
        controls=[btn_volver],
        alignment=ft.MainAxisAlignment.START
    )
    toolbar = ft.Row(
        controls=[toolbar_left],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    

    grid_pagos = ft.GridView(
        expand=True,
        max_extent=250,
        runs_count=3,  # Cantidad de columnas en la cuadrícula
        spacing=10,
        run_spacing=10,
    )

    main_column = ft.Column(
        controls=[toolbar, grid_pagos],
        spacing=10,
        expand=True,
    )

    # Wrap in one Container and return it
    gestionar_pagos_user_container = ft.Container(
        content=main_column,
        gradient=ft.LinearGradient(
            colors=[ft.Colors.WHITE, ft.Colors.BLUE_200],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        ),
        expand=True,
        padding=20,
    )

    page.run_task(getPagos)


    return gestionar_pagos_user_container

# Exportamos la función con el alias 'Gestionar_pagos'
Gestionar_pagos_user = gestionar_pagos_user_view

__all__ = ["gestionar_pagos"]
