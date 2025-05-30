import flet as ft
from utils.ConexionDB             import api_client
from utils.global_state           import auth_state

def logout(page: ft.Page):
    # Clear global auth state
    auth_state.is_authenticated = False
    auth_state.user = None
    # Navigate away
    page.go("/")
    page.update()

def trainer_menu_view(page: ft.Page):
    # Sidebar with route buttons
    sidebar = ft.Container(
        width=250,
        bgcolor=ft.Colors.BLUE_GREY,
        padding=ft.padding.all(15),
        content=ft.Column(
            controls=[
                ft.ElevatedButton(
                    text="Visualizar Entrenamientos",
                    width=250,
                    on_click=lambda _: page.go("/trainer_trainings"),
                ),
                
                ft.ElevatedButton(
                    text="Visualizar Torneos",
                    width=250,
                    on_click=lambda _: page.go("/visualizar_torneos")
                ),
                
                ft.Divider(color=ft.Colors.WHITE54),
                
                ft.ElevatedButton(
                    "Logout",
                    width=250,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: logout(page)
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Fetch trainer name
    uid = auth_state.user.get("localId", "") if auth_state.user else ""
    try:
        resp = api_client.get(f"personas/uid/{uid}")
        person = resp[0] if isinstance(resp, list) else resp
        welcome_name = person.get("nombre", "Entrenador")
    except:
        welcome_name = "Entrenador"

    # Main content area
    main_content = ft.Container(
        expand=True,
        gradient=ft.LinearGradient([ft.Colors.WHITE, ft.Colors.BLUE_200],
                                  begin=ft.alignment.top_center,
                                  end=ft.alignment.bottom_center),
        content=ft.Column(
            [
                ft.Text(f"Bienvenido, {welcome_name}", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Este es tu menú de entrenador.", size=16),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True
        )
    )

    return ft.Container(
        expand=True,
        content=ft.Column([
            ft.Row(controls=[sidebar, main_content], expand=True),
        ])
    )

Trainer_menu = trainer_menu_view
__all__ = ["trainer_menu"]
