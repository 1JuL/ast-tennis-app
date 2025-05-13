import flet as ft
from pages.gestionar_pagos import Gestionar_pagos
from pages.visualizar_torneos import Visualizar_torneos
from pages.gestionar_entrenamientos import Gestionar_entrenamientos  # Importa la nueva vista de entrenamientos
from pages.visualizar_entrenamientos import Visualizar_entrenamientos  # Importa la nueva vista de entrenamientos
from pages.gestionar_torneos import Gestionar_torneos
from pages.add_user_info import Add_user_info
from pages.gestionar_pagos_user import Gestionar_pagos_user
from pages.trainer_trainings import Trainer_trainings
from pages.user_tournaments import User_tournaments
def nav_buttons(page: ft.Page):

    nav = ft.Container(
        content=ft.Column(
            [
                ft.ElevatedButton(
                    text="Gestionar Pagos",
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: page.go("/gestionar_pagos")
                ),
                ft.ElevatedButton(
                    text="Usuario Torneos",
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: page.go("/user_tournaments")
                ),
                ft.ElevatedButton(
                    text="Profesor Entrenamientos",
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: page.go("/trainer_trainings")
                ),
                ft.ElevatedButton(
                    text="Gestionar Torneos",
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: page.go("/gestionar_torneos")
                ),
                ft.ElevatedButton(
                    text="Visualizar Torneos",
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: page.go("/visualizar_torneos")
                ),
                ft.ElevatedButton(
                    text="Gestionar Entrenamientos", 
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: page.go("/gestionar_entrenamientos")
                ),
                ft.ElevatedButton(
                    text="Visualizar Entrenamientos", 
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: page.go("/visualizar_entrenamientos")
                ),
                ft.ElevatedButton(
                    text="Visualizar Pagos (usuario)",  
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: page.go("/gestionar_pagos_user")
                ),
                ft.ElevatedButton(
                    text="Trainer Trainings",  
                    width=250,
                    bgcolor=ft.Colors.BLACK,
                    on_click=lambda e: page.go("/trainer_trainings")
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="Volver",
                        width=280,
                        bgcolor="white",
                        on_click=lambda e: page.go("/")
                    ),
                    padding=ft.padding.only(20, 20)
                )
                # Agrega más botones según lo necesites...
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(20)
    )
    
    return nav

# Exportamos la función con el alias 'nav_buttons'
Nav_buttons = nav_buttons

__all__ = ["nav_buttons"]
