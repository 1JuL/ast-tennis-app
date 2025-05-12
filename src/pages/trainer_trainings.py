import flet as ft
import requests
from utils.ConexionDB import api_client

def trainer_trainings(page: ft.Page):
    # Variable de estado para almacenar todos los entrenamientos
    entrenamientos = []

    # Función para obtener estudiantes por categoría
    def obtener_estudiantes_por_categoria(categoria):
        try:
            response = api_client.get("personas")
            print(f"Respuesta de /personas: {len(response)} personas")  # Depurar
            estudiantes = [p for p in response if p.get('rol') == "Usuario" and p.get('categoria') == categoria]
            print(f"Estudiantes encontrados para categoría {categoria}: {estudiantes}")  # Depurar
            return estudiantes
        except Exception as e:
            print(f"Error al obtener estudiantes: {e}")
            return []

    # Función para obtener estudiantes inscritos en un entrenamiento
    def obtener_estudiantes_inscritos(entrenamiento_id):
        try:
            print(f"Solicitando participantes para evento {entrenamiento_id}")
            response = api_client.get("personasEventos", params={"eventoId": entrenamiento_id})
            print(f"Respuesta de participantes: {response}")
            return response if response else []
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Evento {entrenamiento_id} no tiene participantes")
                return []
            print(f"Error al obtener estudiantes inscritos: {e}")
            return []
        except Exception as e:
            print(f"Error al obtener estudiantes inscritos: {e}")
            return []

    # Función para añadir estudiante
    def añadir_estudiante(entrenamiento_id, persona_uid):
        try:
            print(f"Añadiendo estudiante {persona_uid} al evento {entrenamiento_id}")
            response = api_client.post(
                "personasEventos",
                data={"eventoId": entrenamiento_id, "personaUid": persona_uid}
            )
            print(f"Respuesta del servidor: {response}")  # Depurar respuesta completa
            page.snack_bar = ft.SnackBar(ft.Text("Estudiante añadido"), bgcolor=ft.Colors.GREEN_600)
            page.snack_bar.open = True
            page.update()
            return True
        except requests.exceptions.HTTPError as e:
            error_text = e.response.text if e.response.text else "No se recibió mensaje de error del servidor"
            print(f"Error al añadir estudiante: {e.response.status_code} - {error_text}")  # Depurar detalles del error
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error al añadir estudiante: {e.response.status_code} - {error_text}"),
                bgcolor=ft.Colors.RED_600
            )
            page.snack_bar.open = True
            page.update()
            return False
        except Exception as e:
            print(f"Error al añadir estudiante: {e}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al añadir estudiante: {e}"), bgcolor=ft.Colors.RED_600)
            page.snack_bar.open = True
            page.update()
            return False

    # Función para eliminar estudiante
    def eliminar_estudiante(participante_id):
        try:
            response = api_client.delete(f"personasEventos/{participante_id}")
            page.snack_bar = ft.SnackBar(ft.Text("Estudiante eliminado"), bgcolor=ft.Colors.GREEN_600)
            page.snack_bar.open = True
            page.update()
            return True
        except requests.exceptions.HTTPError as e:
            print(f"Error al eliminar estudiante: {e}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar estudiante: {e.response.status_code}"), bgcolor=ft.Colors.RED_600)
            page.snack_bar.open = True
            page.update()
            return False
        except Exception as e:
            print(f"Error al eliminar estudiante: {e}")
            page.snack_bar = ft.SnackBar(ft.Text("Error al eliminar estudiante"), bgcolor=ft.Colors.RED_600)
            page.snack_bar.open = True
            page.update()
            return False

    # Función para actualizar asistencia
    def actualizar_asistencia(participante_id, asistencia):
        try:
            response = api_client.put(
                f"personasEventos/{participante_id}",
                data={"asistencia": asistencia}
            )
            page.snack_bar = ft.SnackBar(ft.Text("Asistencia actualizada"), bgcolor=ft.Colors.GREEN_600)
            page.snack_bar.open = True
            page.update()
        except requests.exceptions.HTTPError as e:
            print(f"Error al actualizar asistencia: {e}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar asistencia: {e.response.status_code}"), bgcolor=ft.Colors.RED_600)
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            print(f"Error al actualizar asistencia: {e}")
            page.snack_bar = ft.SnackBar(ft.Text("Error al actualizar asistencia"), bgcolor=ft.Colors.RED_600)
            page.snack_bar.open = True
            page.update()

    # Diálogo para gestionar asistencia
    def mostrar_dialogo_asistencia(entrenamiento):
        print("Abriendo diálogo de asistencia")  # Depurar
        estudiantes = obtener_estudiantes_inscritos(entrenamiento['id'])
        lista = ft.ListView(expand=True, spacing=10, padding=10)
        
        if not estudiantes:
            lista.controls.append(ft.Text("No hay estudiantes inscritos", italic=True, color=ft.Colors.GREY_600))
        else:
            for estudiante in estudiantes:
                lista.controls.append(
                    ft.ListTile(
                        title=ft.Text(
                            f"{estudiante.get('persona', {}).get('nombre', 'Desconocido')} {estudiante.get('persona', {}).get('apellido', '')}",
                            weight="bold"
                        ),
                        trailing=ft.Switch(
                            value=estudiante.get('asistencia', False),
                            on_change=lambda e, pid=estudiante['id']: actualizar_asistencia(
                                pid, 
                                e.control.value
                            )
                        )
                    )
                )
        
        dialog = ft.AlertDialog(
            title=ft.Text(f"Asistencia: {entrenamiento['nombre']}"),
            content=ft.Container(content=lista, height=300, width=400, bgcolor=ft.Colors.WHITE),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialog), style=ft.ButtonStyle(color=ft.Colors.BLUE_700))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(dialog)
        print("Diálogo de asistencia abierto")  # Depurar
        page.update()

    # Diálogo para añadir/eliminar estudiantes (pop-up)
    def abrir_dialogo_añadir(entrenamiento):
        print(f"Cargando diálogo para evento {entrenamiento['id']} con categoría {entrenamiento['categoria']}")  # Depurar
        estudiantes_inscritos = obtener_estudiantes_inscritos(entrenamiento['id'])
        estudiantes_disponibles = obtener_estudiantes_por_categoria(entrenamiento['categoria'])
        inscritos_uids = {e['personaUid'] for e in estudiantes_inscritos}
        estudiantes_disponibles = [e for e in estudiantes_disponibles if e['uid'] not in inscritos_uids]

        # Lista de estudiantes disponibles
        lista_disponibles = ft.ListView(expand=True, spacing=10, padding=10)
        if not estudiantes_disponibles:
            lista_disponibles.controls.append(ft.Text("No hay estudiantes disponibles en esta categoría", italic=True, color=ft.Colors.GREY_600))
        else:
            for estudiante in estudiantes_disponibles:
                lista_disponibles.controls.append(
                    ft.ListTile(
                        title=ft.Text(
                            f"{estudiante.get('nombre', 'Desconocido')} {estudiante.get('apellido', '')}",
                            weight="bold"
                        ),
                        subtitle=ft.Text(f"Categoría: {estudiante.get('categoria', 'Sin categoría')}"),
                        trailing=ft.IconButton(
                            icon=ft.Icons.ADD_CIRCLE,
                            icon_color=ft.Colors.GREEN_600,
                            tooltip="Añadir estudiante",
                            on_click=lambda e, uid=estudiante['uid']: [
                                añadir_estudiante(entrenamiento['id'], uid) and actualizar_dialogo_añadir(dialog, entrenamiento)
                            ]
                        ),
                        bgcolor=ft.Colors.BLUE_50,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )

        # Lista de estudiantes inscritos
        lista_inscritos = ft.ListView(expand=True, spacing=10, padding=10)
        if not estudiantes_inscritos:
            lista_inscritos.controls.append(ft.Text("No hay estudiantes inscritos", italic=True, color=ft.Colors.GREY_600))
        else:
            for estudiante in estudiantes_inscritos:
                lista_inscritos.controls.append(
                    ft.ListTile(
                        title=ft.Text(
                            f"{estudiante.get('persona', {}).get('nombre', 'Desconocido')} {estudiante.get('persona', {}).get('apellido', '')}",
                            weight="bold"
                        ),
                        trailing=ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED_600,
                            tooltip="Eliminar estudiante",
                            on_click=lambda e, pid=estudiante['id']: [
                                eliminar_estudiante(pid) and actualizar_dialogo_añadir(dialog, entrenamiento)
                            ]
                        ),
                        bgcolor=ft.Colors.BLUE_50,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )

        contenido = ft.Column([
            ft.Text("Estudiantes Disponibles", weight="bold", size=16, color=ft.Colors.BLUE_900),
            ft.Container(
                content=lista_disponibles,
                height=200,
                width=450,
                border=ft.border.all(1, ft.Colors.BLUE_200),
                border_radius=8,
                bgcolor=ft.Colors.WHITE
            ),
            ft.Text("Estudiantes Inscritos", weight="bold", size=16, color=ft.Colors.BLUE_900),
            ft.Container(
                content=lista_inscritos,
                height=200,
                width=450,
                border=ft.border.all(1, ft.Colors.BLUE_200),
                border_radius=8,
                bgcolor=ft.Colors.WHITE
            )
        ], spacing=15)

        dialog = ft.AlertDialog(
            title=ft.Text(f"Gestionar Estudiantes: {entrenamiento['nombre']}", weight="bold", color=ft.Colors.BLUE_900),
            content=ft.Container(content=contenido, height=450, width=450, padding=10),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialog), style=ft.ButtonStyle(color=ft.Colors.BLUE_700))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.BLUE_50
        )
        print("Abriendo diálogo de añadir estudiantes")  # Depurar
        page.open(dialog)
        print("Diálogo de añadir estudiantes abierto")  # Depurar
        page.update()

    # Funciones auxiliares
    def actualizar_dialogo_añadir(dialog, entrenamiento):
        print("Actualizando diálogo de añadir estudiantes")  # Depurar
        page.close(dialog)
        page.update()
        abrir_dialogo_añadir(entrenamiento)

    def cerrar_dialogo(dialog):
        print("Cerrando diálogo")  # Depurar
        page.close(dialog)
        page.update()

    def obtener_nombre_profesor_por_id(uid):
        try:
            response = api_client.get(f"personas/{uid}")
            return f"{response.get('nombre', 'Desconocido')} {response.get('apellido', '')}"
        except Exception as e:
            print(f"Error al obtener profesor: {e}")
            return "Desconocido"

    def obtener_entrenamientos_tipo_2():
        try:
            response = api_client.get("eventos")
            print(f"Respuesta de /eventos: {response}")
            if not isinstance(response, list):
                print("Error: Respuesta no es una lista")
                return []
            entrenamientos = [e for e in response if e.get('tipo') == 2]
            print(f"Entrenamientos encontrados: {entrenamientos}")
            return entrenamientos
        except Exception as e:
            print(f"Error al obtener eventos: {e}")
            return []

    # Función para buscar entrenamientos
    def buscar_entrenamientos(e):
        filtro = search_field.value.lower() if search_field.value else ""
        filtered_entrenamientos = [
            entrenamiento for entrenamiento in entrenamientos
            if filtro in entrenamiento["nombre"].lower()
        ]
        grid.controls.clear()
        for entrenamiento in filtered_entrenamientos:
            grid.controls.append(crear_card_entrenamiento(entrenamiento))
        page.update()

    # Crear tarjeta de entrenamiento
    def crear_card_entrenamiento(entrenamiento):
        profesor = obtener_nombre_profesor_por_id(entrenamiento.get('profesorID', ''))
        botones = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Añadir Estudiantes",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=lambda e: abrir_dialogo_añadir(entrenamiento),
                    bgcolor=ft.Colors.GREEN_400,
                    color=ft.Colors.WHITE
                ),
                ft.ElevatedButton(
                    "Dar Asistencia",
                    icon=ft.Icons.CHECKLIST,
                    on_click=lambda e: mostrar_dialogo_asistencia(entrenamiento),
                    bgcolor=ft.Colors.ORANGE_400,
                    color=ft.Colors.WHITE
                )
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(entrenamiento.get('nombre', 'Sin nombre'), size=20, weight="bold", color=ft.Colors.BLUE_900),
                    ft.Text(f"Fecha: {entrenamiento.get('fecha', 'Sin fecha')}", color=ft.Colors.GREY_800),
                    ft.Text(f"Categoría: {entrenamiento.get('categoria', 'Sin categoría')}", color=ft.Colors.GREY_800),
                    ft.Text(f"Profesor: {profesor}", color=ft.Colors.GREY_800),
                    botones
                ], spacing=10),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=8
            ),
            elevation=5,
            width=300
        )

    # Interfaz principal
    # Obtener entrenamientos inicialmente
    entrenamientos = obtener_entrenamientos_tipo_2()
    grid = ft.GridView(expand=True, max_extent=300, spacing=20, run_spacing=20, padding=20)
    for entrenamiento in entrenamientos:
        grid.controls.append(crear_card_entrenamiento(entrenamiento))

    # Botón de volver (asumido como parte de la interfaz)
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_600,
        tooltip="Volver",
        on_click=lambda e: page.go("/"),  # Ajusta la ruta según tu lógica
    )

    # Campo de búsqueda
    search_field = ft.TextField(
        hint_text="Filtrar por nombre de torneo",
        width=300,
        color=ft.Colors.BLACK,
        hint_style=ft.TextStyle(color=ft.Colors.BLACK54),
        border_color=ft.Colors.BLUE_600,
        on_submit=buscar_entrenamientos
    )

    # Ícono de búsqueda
    search_icon = ft.IconButton(
        icon=ft.Icons.SEARCH,
        icon_color=ft.Colors.BLUE_600,
        tooltip="Buscar",
        on_click=buscar_entrenamientos
    )

    # Contenedor de búsqueda
    search_container = ft.Row(
        controls=[
            search_field,
            search_icon
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START
    )

    # Barra de herramientas
    toolbar = ft.Row(
        controls=[
            btn_volver,
            search_container,
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Contenedor principal
    return ft.Container(
        content=ft.Column([
            ft.AppBar(
                title=ft.Text("Entrenamientos", weight="bold"),
                bgcolor=ft.Colors.BLUE_400,
                color=ft.Colors.WHITE,
                actions=[toolbar]  # Agregamos la barra de herramientas al AppBar
            ),
            ft.Row([search_container]),  # Mostramos el campo de búsqueda por separado si lo deseas
            grid
        ]),
        gradient=ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_100]),
        padding=10
    )

Trainer_trainings = trainer_trainings
__all__ = ["Trainer_trainings"]