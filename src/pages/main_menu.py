import flet as ft
from pages.gestionar_torneos import Gestionar_torneos
from pages.gestionar_pagos import Gestionar_pagos
from pages.gestionar_entrenamientos import Gestionar_entrenamientos

class Sidebar(ft.Container):
    def __init__(self, page: ft.Page):
        # Definimos las opciones de navegación
        destinations = [
            ft.NavigationRailDestination(
                label="Gestionar Entrenamientos",
                icon=ft.Icons.FITNESS_CENTER,
                selected_icon=ft.Icons.FITNESS_CENTER
            ),
            ft.NavigationRailDestination(
                label="Gestionar Pagos",
                icon=ft.Icons.PAYMENT,
                selected_icon=ft.Icons.PAYMENT
            ),
            ft.NavigationRailDestination(
                label="Gestionar Torneos",
                icon=ft.Icons.SPORTS_TENNIS,
                selected_icon=ft.Icons.SPORTS_TENNIS
            )
        ]
        self.nav_rail = ft.NavigationRail(
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=destinations,
            selected_index=0,
            on_change=lambda e: self.on_nav_change(e, page)
        )
        # Envolvemos el NavigationRail en un Container con altura fija para solucionar el error de altura no definida
        nav_container = ft.Container(content=self.nav_rail, height=600)
        super().__init__(
            content=ft.Column(
                controls=[
                    ft.Text("Navegación", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Divider(color=ft.Colors.WHITE54),
                    nav_container
                ],
                spacing=10,
            ),
            width=250,
            bgcolor=ft.Colors.BLUE_GREY,
            padding=ft.padding.all(15),
        )
        


    def on_nav_change(self, e, page: ft.Page):
        index = e.control.selected_index
        if index == 0:
            page.views.append(
            ft.View(
                route="/gestionar_entrenamientos",
                controls=[Gestionar_entrenamientos(page)]
                )
            )
            page.go("/gestionar_entrenamientos")
        elif index == 1:
            page.views.append(
            ft.View(
                route="/gestionar_pagos",
                controls=[Gestionar_pagos(page)]
                )
            )
            page.go("/gestionar_pagos")
        elif index == 2:
            page.views.append(
            ft.View(
                route="/gestionar_torneos",
                controls=[Gestionar_torneos(page)]
                )
            )
            page.go("/gestionar_torneos")
        page.update()

def main_menu_view(page: ft.Page):
    
    def on_back(e):
        page.clean()
        page.controls = [layout]
        page.update()
    
    # Configuramos un AppBar (opcional)
    page.appbar = ft.AppBar(
        title=ft.Text("Main Menu"),
        bgcolor=ft.Colors.BLUE_GREY,
    )

    # Creamos el sidebar
    sidebar = Sidebar(page)
    
    # Definimos el contenido principal
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Bienvenido al Main Menu", size=30, weight=ft.FontWeight.BOLD, text_align="center"),
                ft.ElevatedButton(
                    text="Salir",
                    width=250,
                    bgcolor=ft.Colors.RED,
                    on_click=lambda e: page.window.close()
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        expand=True,
        alignment=ft.alignment.center
    )

    layout = ft.Row(
        controls=[sidebar, main_content],
        expand=True
    )
    
    return layout

Main_menu = main_menu_view
__all__ = ["main_menu"]
