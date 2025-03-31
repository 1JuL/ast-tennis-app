import flet as ft
from models.Payment import Payment  # Ajusta la ruta según tu estructura de carpetas
from utils.ConexionDB import api_client
import datetime

def gestionar_pagos_view(page: ft.Page):
   
    def getEstudiantes():
        """Consigue los estudiantes desde la api y se cargan en una lista retornada"""
        listaEstudiantes = []
        response = api_client.get("personas")
        for usuario in response:
            if usuario["rol"] == "Estudiante" or usuario["rol"] == "Usuario" :
                listaEstudiantes.append(usuario)
        return listaEstudiantes


    def cargarUsuariosCombo():
        """ se cargan los usuarios al combox box """
        options = []
        studentsList = getEstudiantes()
        for student in studentsList:
            options.append(ft.DropdownOption(key=student["id"], content=ft.Text(value=f"{student["nombre"]} {student["apellido"]}")))
        return options
    

    def getPagos(id):
        """Se piden los pagos de la persona mediante su id y se cargan en el gridView"""
        try:
            pagos = api_client.get(f"pagos/usuario/{id}")
            pagosUsuario = [] # en este arreglo se cargarán los objetos tipo Payment del usuario
            for pago in pagos:
                pagosUsuario.append(Payment(pago["id"],pago["personalID"], pago["monto"], pago["fecha"], pago["estado"]))
            cargar_pagos(pagosUsuario)
        except:
            print("error al cargar los datos")


    def crear_card_pago(pago: Payment):
        """ retorna la tarjeta de un pago """
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"ID: {pago.ID}", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(f"ID Persona: {pago.personaId}"),
                        ft.Text(f"Monto: ${pago.monto:.2f}"),
                        ft.Text(f"Fecha: {pago.fecha}"),
                        ft.Text(
                            f"Estado: {pago.estado}",
                            color=ft.Colors.AMBER_500 if pago.estado == 'Pendiente' else ft.Colors.GREEN_500
                        )
                    ],
                    spacing=5,
                ),
                padding=10,
                bgcolor=ft.Colors.SURFACE,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                border=ft.border.all(2, ft.Colors.AMBER_500 if pago.estado == 'Pendiente' else ft.Colors.GREEN_500),
            ),
            elevation=2,
            height=30
        )

    def cargar_pagos(pagos):
        """carga los pagos en el grid"""
        grid_pagos.controls.clear()
        for pago in pagos:
            grid_pagos.controls.append(crear_card_pago(pago))
    
    def registrar_pago(e):
        # Aquí puedes manejar la lógica para guardar los datos, etc.
        api_client.post("pagos/", )
        # Cerramos el diálogo después de registrar
        page.close(dialogReg)
    
    def registrar_pago_id(e):
        # Aquí puedes manejar la lógica para guardar los datos, etc.
        api_client.post("pagos/", )
        # Cerramos el diálogo después de registrar
        page.close(dialogRegId)
    
    def handle_change(e: ft.ControlEvent):
        if e.data is not None:  # Si se seleccionó una fecha
            fecha_input.value = e.control.value.strftime('%Y-%m-%d')
            page.update()

    def open_date_picker(e):
        page.open(ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=10, day=1),
                    last_date=datetime.datetime(year=2024, month=10, day=1),
                    on_change=handle_change,
                ))

    # Barra de herramientas
    combo = ft.Dropdown(
        options = cargarUsuariosCombo(),
        hint_text="Seleccione",
        border_color= ft.Colors.TRANSPARENT)
    
    combo_registro = combo

    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: page.on_back() if hasattr(page, "on_back") else None
    )
    btn_buscar = ft.ElevatedButton("Buscar", on_click=lambda e: getPagos(combo.value), bgcolor= ft.Colors.SURFACE)
    btn_registrar = ft.ElevatedButton("Registrar pago", on_click=lambda e: page.open(dialogReg), color=ft.Colors.GREEN_500, bgcolor= ft.Colors.SURFACE)
    btn_registrar_id = ft.ElevatedButton("Registrar pago por ID", on_click=lambda e: page.open(dialogRegId), color=ft.Colors.AMBER_500,bgcolor= ft.Colors.SURFACE)

    toolbar_left = ft.Row(
        controls=[btn_volver, combo, btn_buscar],
        alignment=ft.MainAxisAlignment.START
    )
    toolbar_right = ft.Row(
        controls=[btn_registrar, btn_registrar_id],
        alignment=ft.MainAxisAlignment.END
    )
    toolbar = ft.Row(
        controls=[toolbar_left, toolbar_right],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    grid_pagos = ft.GridView(
        expand=True,
        max_extent=250,
        runs_count=3,  # Cantidad de columnas en la cuadrícula
        spacing=10,
        run_spacing=10,
    )

    # controles para modal registro de pago
    monto_input = ft.TextField(
        label="Monto",
        hint_text="Ingrese el monto del pago",
        width=300
    )

    fecha_input = ft.TextField(
        label="Fecha de Pago",
        hint_text="dd/mm/aaaa",
        read_only=True,
        width=300,
        on_click= open_date_picker
                
    )

    estado_dropdown = ft.Dropdown(
        label="Estado",
        hint_text="Seleccione un estado",
        options=[
            ft.dropdown.Option("Pendiente"),
            ft.dropdown.Option("Pagado"),
            ft.dropdown.Option("Cancelado"),
        ],
        width=300
    )
    #Ventana de díalogo registro de pago
    dialogReg = ft.AlertDialog(
        modal=True,  # Hace que sea una ventana modal
        title=ft.Text("Registrar Pago", size=20, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                combo_registro,
                monto_input,
                fecha_input,
                estado_dropdown
            ],
            tight=True,            # Ajusta el espacio vertical
            horizontal_alignment=ft.CrossAxisAlignment.START
        ),
        actions_alignment="end",  # Alinea los botones a la derecha
        actions=[
            ft.TextButton(
                "Cancelar", 
                on_click=lambda e: (
                    page.close(dialogReg)
                )
            ),
            ft.TextButton(
                "Registrar Pago",
                on_click=registrar_pago
            ),
        ],
        # Puedes ajustar el ancho máximo si deseas:
        # width=400
    )
    input_id = ft.TextField(label="Monto", hint_text="Ingrese el monto del pago", width=300)


    dialogRegId = ft.AlertDialog(
        modal=True,  # Hace que sea una ventana modal
        title=ft.Text("Registrar Pago por ID", size=20, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                input_id
            ],
            tight=True,            # Ajusta el espacio vertical
            horizontal_alignment=ft.CrossAxisAlignment.START
        ),
        actions_alignment="end",  # Alinea los botones a la derecha
        actions=[
                ft.TextButton(
                "Cancelar", 
                on_click=lambda e: (
                    page.close(dialogRegId)
                )
            ),
            ft.TextButton(
                "Registrar Pago",
                on_click=registrar_pago_id
            ),
        ],
        # Puedes ajustar el ancho máximo si deseas:
        # width=400
    )


    # Construcción del contenedor principal que une la barra de herramientas y el grid
    main_container = ft.Container(
        content=ft.Column(
        controls=[toolbar, grid_pagos],
        spacing=10,
        expand= True, 
        ),
        gradient= ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_200], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
        expand=True,
    )
    return main_container

# Exportamos la función con el alias 'Gestionar_pagos'
Gestionar_pagos = gestionar_pagos_view

__all__ = ["gestionar_pagos"]
