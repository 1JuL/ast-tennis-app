import flet as ft
from utils.firebase        import sign_in
from utils.global_state   import auth_state
from utils.ConexionDB      import api_client

def login_view(page: ft.Page):
    # Input fields
    email_input = ft.TextField(
        label="Correo",
        prefix_icon=ft.Icons.EMAIL,
        color="black",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
    )
    password_input = ft.TextField(
        label="Contraseña",
        password=True,
        prefix_icon=ft.Icons.LOCK,
        color=ft.Colors.BLACK,
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_500),
        content_padding=ft.padding.only(bottom=15),
    )

    # Spinner
    spinner = ft.ProgressRing(visible=False)

    # Handlers
    def handle_login(e):
        spinner.visible = True
        page.update()

        user = sign_in(email_input.value, password_input.value)

        if user:
            auth_state.is_authenticated = True
            auth_state.user = user
            uid = user.get("localId")

            # Fetch role
            try:
                personas = api_client.get(f"personas/uid/{uid}")
                persona  = personas[0] if isinstance(personas, list) else personas
                rol      = persona.get("rol", "user")
                
                dlg = ft.AlertDialog(
                    title=ft.Text("Éxito"),
                    content=ft.Text("Inicio de sesión exitoso"),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: on_success(e, dlg, rol))
                    ]
                )
            except:
                rol = "null"
                auth_state.is_authenticated = False
                auth_state.user = None
                dlg = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("No se pudo obtener un rol valido"),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: page.go("/"))
                    ]
                )
            
            page.open(dlg)                

            
        else:
            auth_state.is_authenticated = False
            auth_state.user = None
            dlg = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("No se pudo iniciar sesión"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: close_error(e, dlg))
                ]
            )

        page.open(dlg)

    def close_error(e, dlg):
        spinner.visible = False
        page.update()
        dlg.open = False
        page.update()

    def on_success(e, dlg, rol):
        spinner.visible = False
        page.update()
        dlg.open = False
        page.update()
        # route-based navigation
        if rol == "admin":
            page.go("/admin_menu")
        elif rol == "Profesor":
            page.go("/trainer_menu")
        elif rol == "user":
            page.go("/user_menu")

    def go_back(e):
        page.go("/")

    # Build UI
    login_container = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            colors=[ft.Colors.WHITE, ft.Colors.BLUE_200],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        ),
        content=ft.Column(
            [
                ft.Column(
                    [
                        ft.Text("Iniciar sesión",
                                size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                        ft.Text("Hola de nuevo",
                                size=16, color=ft.Colors.BLACK54),
                    ],
                    horizontal_alignment="center"
                ),
                ft.Column(
                    [
                        ft.Row(controls=[email_input], alignment="center"),
                        ft.Row(controls=[password_input], alignment="center"),
                        spinner,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    [
                        ft.ElevatedButton(
                            "Iniciar Sesión",
                            height=50, width=250,
                            color="#0F3BAC",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                            bgcolor="#FEF7FF",
                            on_click=handle_login
                        ),
                        ft.ElevatedButton(
                            "Volver",
                            height=50, width=250,
                            bgcolor="#ffcccc", color="red",
                            on_click=go_back
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    return login_container

Login = login_view
__all__ = ["login"]
