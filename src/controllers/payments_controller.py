from views.payments_view import PaymentsView
from models.Payment import Payment
import flet as ft

class PaymentsController:
    
    def __init__(self, view:PaymentsView):
        self.view = view
        
    def crear_card_pago(pago: Payment):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"ID: {pago.ID}", weight=ft.FontWeight.BOLD, color=ft.Colors),
                        ft.Text(f"ID Persona: {pago.personaId}"),
                        ft.Text(f"Monto: ${pago.monto:.2f}"),
                        ft.Text(f"Fecha: {pago.fecha}"),
                        ft.Text(f"Estado: {pago.estado}", color= ft.Colors.AMBER_500 if pago.estado == 'Pendiente' else ft.Colors.GREEN_500)
                        
                    ],
                    spacing=5,
                    
                ),
                padding=10,
                bgcolor= ft.Colors.BLACK,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                border=ft.border.all(2,ft.Colors.AMBER_500 if pago.estado == 'Pendiente' else ft.Colors.GREEN_500),
            ),
            elevation=2,
            height= 30
        )
   
    def cargarPagos(self, pagos):
           for pago in pagos:
            self.view.grid_pagos.controls.append(self.crear_card_pago(pago))
