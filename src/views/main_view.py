import flet as ft

class MainView:
    def __init__(self, controller):
        self.controller = controller
        
        # Botón para navegar a la pantalla de registro
        self.btn_registration = ft.ElevatedButton(
            "Ir a Registro",
            on_click=self.on_registration_click
        )
        
        self.view = ft.Column(
            [
                ft.Text("Menú Principal", style="headlineMedium"),
                self.btn_registration,
                # Puedes agregar más botones para otros componentes
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True
        )
        
    def on_registration_click(self, e):
        self.controller.go_to_registration()
