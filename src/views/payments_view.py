import flet as ft
from ..models.Payment import Payment

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
        self.cargarPagos([Payment(1,1,28000,'28-10-2025'),Payment(1,1,30000,'28-10-2025',"Pagado")])# esto es pa simular, pero insitu recibe una lista
        
    
    def crear_card_pago(pago: Payment):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"ID: {pago.ID}", weight=ft.FontWeight.BOLD, color=ft.colors),
                        ft.Text(f"ID Persona: {pago.personaId}"),
                        ft.Text(f"Monto: ${pago.monto:.2f}"),
                        ft.Text(f"Fecha: {pago.fecha}"),
                        ft.Text(f"Estado: {pago.estado}", color= ft.colors.AMBER_500 if pago.estado == 'Pendiente' else ft.colors.GREEN_500)
                        
                    ],
                    spacing=5,
                    
                ),
                padding=10,
                bgcolor= ft.colors.BLACK,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12),
                border=ft.border.all(2,ft.colors.AMBER_500 if pago.estado == 'Pendiente' else ft.colors.GREEN_500),
            ),
            elevation=2,
            height= 30
        )
   
    def cargarPagos(self, pagos):
           for pago in pagos:
            self.view.grid_pagos.controls.append(self.crear_card_pago(pago))

        
        