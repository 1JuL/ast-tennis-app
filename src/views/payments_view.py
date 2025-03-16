import flet as ft

class PaymentsView:
    
    def __init__(self, controller):
        self.controller = controller
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
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Volver",
                )
        
        btn_buscar = ft.ElevatedButton("Buscar", on_click=lambda e: print("Buscar"))

        btn_registrar = ft.ElevatedButton("Registrar pago", on_click=lambda e: print("Registrar pago"), color= ft.Colors.GREEN_500)
        btn_registrar_id = ft.ElevatedButton("Registrar pago por ID", on_click=lambda e: print("Registrar pago por ID"), color= ft.Colors.AMBER_500)

        toolbar = ft.Row(
            controls=[
                ft.Row([btn_volver,combo, btn_buscar], alignment=ft.MainAxisAlignment.START),
                ft.Row([btn_registrar, btn_registrar_id], alignment=ft.MainAxisAlignment.END),
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
        
        
        
        