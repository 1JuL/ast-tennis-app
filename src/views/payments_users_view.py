import flet as ft

class PaymentsView:
    
    def __init__(self, controller):
        self.controller = controller
        # Barra de herramientas
        btn_volver = ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Volver",
                )
        toolbar = ft.Row(
            controls=[
                ft.Row([btn_volver], alignment=ft.MainAxisAlignment.START),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        grid_pagos = ft.GridView(
            expand=True,
            max_extent=250,
            runs_count=3,  # Cantidad de columnas en la cuadrícula
            spacing=10,
            run_spacing=10,
        )
        
        self.view = ft.Container([toolbar,grid_pagos])
        
        
        
        