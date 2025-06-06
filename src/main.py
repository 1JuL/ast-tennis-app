import flet as ft

from pages.gestionar_entrenamientos import Gestionar_entrenamientos
from pages.gestionar_pagos import Gestionar_pagos
from pages.gestionar_pagos_user import Gestionar_pagos_user
from pages.gestionar_torneos import Gestionar_torneos
from pages.login          import Login
from pages.registration   import Registration
from pages.add_user_info import Add_user_info
from pages.admin_menu     import Admin_menu
from pages.trainer_trainings import Trainer_trainings
from pages.user_menu      import User_menu
from pages.trainer_menu   import Trainer_menu
from pages.user_tournaments import User_tournaments
from pages.visualizar_entrenamientos import Visualizar_entrenamientos
from pages.visualizar_torneos import Visualizar_torneos
from pages.register_person import Register_person

def main(page: ft.Page):
    page.window.maximized = True
    page.title               = "AST Tennis"
    page.bgcolor             = ft.Colors.WHITE
    page.padding             = 0
    page.horizontal_alignment = "stretch"
    page.vertical_alignment   = "stretch"

    # --- on_route_change handler ---
    def route_change(e):
        # Clear out old views
        page.views.clear()

        # Always show the home view
        page.views.append(
            ft.View(
                route="/",
                controls=build_home()
            )
        )
        # Conditionally add the matched view on top
        if page.route == "/login":
            page.views.append(
                ft.View(
                    route="/login",
                    controls=[ Login(page) ]
                )
            )
        elif page.route == "/register":
            page.views.append(
                ft.View(
                    route="/register",
                    controls=[ Registration(page) ]
                )
            )
        elif page.route == "/add_user_info":
            page.views.append(
                ft.View(
                    route="/add_user_info", 
                    controls=[ Add_user_info(page) ]
                )
            )
        elif page.route == "/admin_menu":
            page.views.append(
                ft.View(
                    route="/admin_menu",
                    controls=[ Admin_menu(page) ]
                )
            )
        elif page.route == "/user_menu":
            page.views.append(
                ft.View(
                    route="/user_menu",
                    controls=[ User_menu(page) ]
                )
            )
        elif page.route == "/trainer_menu":
            page.views.append(
                ft.View(
                    route="/trainer_menu",
                    controls=[ Trainer_menu(page) ]
                )
            )
        elif page.route == "/gestionar_entrenamientos":
            page.views.append(
                ft.View(
                    route="/gestionar_entrenamientos",
                    controls=[ Gestionar_entrenamientos(page) ]
                )
            )
        elif page.route == "/gestionar_torneos":
            page.views.append(
                ft.View(
                    route="/gestionar_torneos",
                    controls=[ Gestionar_torneos(page) ]
                )
            )
        elif page.route == "/gestionar_pagos":
            page.views.append(
                ft.View(
                    route="/gestionar_pagos",
                    controls=[ Gestionar_pagos(page) ]
                )
            )
        elif page.route == "/gestionar_pagos_user":
            page.views.append(
                ft.View(
                    route="/gestionar_pagos_user",
                    controls=[ Gestionar_pagos_user(page) ]
                )
            )
        elif page.route == "/visualizar_entrenamientos":
            page.views.append(
                ft.View(
                    route="/visualizar_entrenamientos",
                    controls=[ Visualizar_entrenamientos(page) ]
                )
            )
        elif page.route == "/visualizar_torneos":
            page.views.append(
                ft.View(
                    route="/visualizar_torneos",
                    controls=[ Visualizar_torneos(page) ]
                )
            )
        elif page.route == "/trainer_trainings":
            page.views.append(
                ft.View(
                    route="/trainer_trainings",
                    controls=[ Trainer_trainings(page) ]
                )
            )
        elif page.route == "/register_person":
            page.views.append(
                ft.View(
                    route="/register_person",
                    controls=[ Register_person(page) ]
                )
            )
        elif page.route == "/user_tournaments":
            page.views.append(
                ft.View(
                    route="/user_tournaments",
                    controls=[ User_tournaments(page) ]
                )
            )

        page.update()

    # --- on_view_pop handler (Back button) ---
    def view_pop(view):
        page.views.pop()              # remove current
        top = page.views[-1]          # peek previous
        page.go(top.route)            # navigate to it

    page.on_route_change = route_change
    page.on_view_pop     = view_pop

    # --- home builder ---
    def build_home():
        return [
            ft.AppBar(title=ft.Text("AST Tennis", size=80, weight=ft.FontWeight.BOLD), center_title=True, toolbar_height=70 ),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Image(src="./src/assets/ast-tennis-logo.png", width=350, height=350),
                    ),
                    ft.Column(
                        [
                            ft.Text("¿Qué vamos a hacer hoy?", size=20),
                            ft.ElevatedButton(
                                "Iniciar sesión",
                                height=50, width=250,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                                on_click=lambda _: page.go("/login")),
                            
                            ft.ElevatedButton(
                                "Registrarse",
                                height=50, width=250,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                                on_click=lambda _: page.go("/register")),
                            
                            ft.ElevatedButton(
                                "Salir",
                                color="white",
                                height=50, width=250,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                                bgcolor=ft.Colors.RED, on_click=lambda _: page.window.close()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=150,
                expand=True
            ),
        ]

    page.go("/")

ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")