import flet as ft
from models.Payment import Payment  # Ajusta la ruta según tu estructura de carpetas
from utils.ConexionDB import api_client
from datetime import datetime
from flet import KeyboardType


def gestionar_pagos_view(page: ft.Page):   
    def getEstudiantes():
        """Consigue los estudiantes desde la api y se cargan en una lista retornada"""
        listaEstudiantes = []
        response = api_client.get("personas")
        for usuario in response:
            if usuario["rol"] == "Estudiante" or usuario["rol"] == "usuario" :
                listaEstudiantes.append(usuario)
        return listaEstudiantes


    def cargarUsuariosCombo():
        """ se cargan los usuarios al combox box """
        options = []
        studentsList = getEstudiantes()
        for student in studentsList:
            usuario = f"{student["nombre"]} {student["apellido"]}"
            options.append(ft.DropdownOption(key=student["id"], content=ft.Text(value=usuario)))
        return options
    
    def eliminarPago(idPago):
        
        dlg_aviso = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar pago"),
            content=ft.Text("Pago eliminado exitósamente"),
            actions=[
                ft.TextButton("Aceptar", on_click=lambda _: page.close(dlg_aviso)),
            ],
            actions_alignment=ft.MainAxisAlignment.END)
        api_client.delete(f"pagos/{idPago}")
        page.open(dlg_aviso)
        grid_pagos.update()
        

    def getPagos(id):
        """Se piden los pagos de la persona mediante su id y se cargan en el gridView"""
        pagosUsuario = [] # en este arreglo se cargarán los objetos tipo Payment del usuario

        dlg_aviso = ft.AlertDialog(
            modal=True,
            title=ft.Text("Aviso"),
            content=ft.Text("No se encontraron pagos para este usuario."),
            actions=[
                ft.TextButton("Aceptar", on_click=lambda _: page.close(dlg_aviso)),
            ],
            actions_alignment=ft.MainAxisAlignment.END)
        
        try:
            pagos = api_client.get(f"pagos/usuario/{id}")
            print(pagos)
            for pago in pagos:
                pagosUsuario.append(Payment(pago["id"],pago["personalID"], float(pago["monto"]), datetime.strptime(pago['fecha'], '%Y-%m-%d') , pago["estado"]))

            print(pagosUsuario)
            cargar_pagos(pagosUsuario)
        except:
            page.open(dlg_aviso)
            grid_pagos.clean()
            grid_pagos.update()
            

    def crear_card_pago(pago: Payment):
        """ retorna la tarjeta de un pago """
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"ID: {pago.ID}", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, selectable=True),
                        ft.Text(f"ID Persona: {pago.personaId}", selectable=True, color=ft.Colors.BLACK),
                        ft.Text(f"Monto: ${pago.monto:.2f}", color=ft.Colors.BLACK),
                        ft.Text(f"Fecha: {pago.fecha}", color=ft.Colors.BLACK),
                        ft.Text(
                            f"Estado: {pago.estado}",
                            color=ft.Colors.AMBER_500 if pago.estado == 'Pendiente' else ft.Colors.GREEN_500,
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.PopupMenuButton(
                                    icon=ft.icons.MORE_VERT,
                                    items=[
                                        ft.PopupMenuItem(
                                            text="Eliminar",
                                            icon=ft.Icons.DELETE,
                                            on_click= lambda _: eliminarPago(pago.ID)
                                        )
                                    ],
                                )
                            ]
                        )
                    ],
                    spacing=5,
                ),
                padding=10,
                bgcolor=ft.Colors.GREY_50,
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
        grid_pagos.update()
    
    def generar_alerta(titulo:str, mensaje:str):
        dlg_aviso = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("Aceptar", on_click=lambda _: page.close(dlg_aviso)),
            ],
            actions_alignment=ft.MainAxisAlignment.END)
        
        return dlg_aviso

    def registrar_pago(lista):
        """Genera una peticion de creacion de pago"""

        # Ya sé que esto se ve horrible pero me rehuso a usar chat para mejorar esta mierda, prefiero esperar a que
        # mi poderoso y sexy cerebro se idee otra forma más optima pa validar esto, por ahora se queda así, total, es mi módulo, puñetas
        if lista[0].strip() == '':
            page.open(generar_alerta("Error", "Debe ingresar un ID"))
            return
        if lista[1].strip() == '':
            page.open(generar_alerta("Error", "Debe ingresar un monto"))
            return
        if lista[2].strip() == '':
            page.open(generar_alerta("Error", "Debe ingresar una fecha"))
            return
        if lista[3].strip() == '':
            page.open(generar_alerta("Error", "Debe seleccionar un estado"))
            return
        
        # si el usuario es serio y no mete burradas se crea el diccionario con los valores
        data = {
        "personalID": lista[0],
        "monto": lista[1],
        "fecha": lista[2],
        "estado": lista[3]
        }
    
        try:
            print(data)
            api_client.post("pagos/",data=data)
            alerta = generar_alerta("Registrar pago", "Pago registrado correctamente!")
            page.open(alerta)
            getPagos(lista[0])
        except :
            alerta = generar_alerta("Error", "No se pudo generar el pago")
            page.open(alerta)
        finally:
            # Cerramos el diálogo después de registrar
            page.close(dialogReg)
            combo_registro.value = None
            monto_input.value = ''
            fecha_input.value = ''
            estado_dropdown.value = None
            

    
    def registrar_pago_id(idPago):
        """ Dado un id de un pago se cambia el estado de ese pago a pagado en caso de que el estado anterior haya sido pendiente"""

        if idPago == '':
            page.open(generar_alerta("Error", "Debe ingresar el id del pago deseado!"))
            return
        
        data = {
            "id": idPago,
            "estado": "Pagado"
        }

        try:
            api_client.put(f"pagos/{idPago}", data=data)
            conf = generar_alerta("Registrar pago", "Pago registrado como \"Pagado\" exitosamente")
            page.open(conf)
        except:
            error = generar_alerta("Error", "No se pudo cambiar el estado del pago")
            page.open(error)
        finally:
            # Cerramos el diálogo después de registrar
            page.close(dialogRegId)
            input_id.value = ''

    
    def handle_change(e: ft.ControlEvent):
        if e.data is not None:  # Si se seleccionó una fecha
            fecha_input.value = e.control.value.strftime('%Y-%m-%d')
            page.update()

    def open_date_picker(e):
        page.open(ft.DatePicker(
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
        on_click=lambda e: page.go("/admin_menu")
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
        width=300,
        keyboard_type = KeyboardType.NUMBER
    )

    fecha_input = ft.TextField(
        label="Fecha de Pago",
        hint_text="aaaa-mm-dd",
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
                on_click=lambda e: registrar_pago([combo_registro.value, monto_input.value, fecha_input.value, estado_dropdown.value])
            ),
        ],

    )
    input_id = ft.TextField(label="Id pago", hint_text="Ingrese el ID del pago", width=300)


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
                on_click=lambda _: registrar_pago_id(input_id.value)
            ),
        ],
    )

    main_column = ft.Column(
        controls=[toolbar, grid_pagos],
        spacing=10,
        expand=True,
    )

    # Wrap in one Container and return it
    gestionar_pagos_container = ft.Container(
        content=main_column,
        gradient=ft.LinearGradient(
            colors=[ft.Colors.WHITE, ft.Colors.BLUE_200],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        ),
        expand=True,
        padding=20,
    )

    return gestionar_pagos_container

# Exportamos la función con el alias 'Gestionar_pagos'
Gestionar_pagos = gestionar_pagos_view

__all__ = ["gestionar_pagos"]
