from views.tournaments_view import TournamentsView
from models.event import Event
from models.event_type import Event_Type
import flet as ft

class TournamentsController:
    
    def __init__(self, view:TournamentsView):
        self.view = view
        
    def crear_card_torneo(torneo: Event, torneo_info: Event_Type):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Nombre: {torneo.nombre}", weight=ft.FontWeight.BOLD, color=ft.Colors),
                        ft.Text(f"Fecha: {torneo.fecha}"),
                        ft.Text(f"Hora: ${torneo.hora}"),
                        ft.Text(f"Podio: ${torneo_info.podio}"),
                    ],
                    spacing=5,
                    
                ),
                padding=10,
                bgcolor= ft.Colors.BLACK,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            ),
            elevation=2,
            height= 30
        )
   
    def cargarTorneos(self, torneos, event_types):
        for event_type in event_types:
            if(event_type.tipo == 1):
                for torneo in torneos:
                    if(torneo.ID == event_type.eventoID):
                        self.view.grid_torneos.controls.append(self.crear_card_torneo(torneo, event_type))