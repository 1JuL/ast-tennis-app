import flet as ft
import requests
from utils.ConexionDB import api_client
from utils.global_state import auth_state

def user_tournaments(page: ft.Page):
    # Obtener el UID desde auth_state.user
    user_data = auth_state.user
    print(f"User data from auth_state: {user_data}")  # Depuración

    if not user_data or 'localId' not in user_data:
        print("Error: UID no disponible en auth_state")
        page.snack_bar = ft.SnackBar(ft.Text("Error: Inicia sesión nuevamente."), bgcolor=ft.Colors.RED_600)
        page.snack_bar.open = True
        page.update()
        return ft.Container(content=ft.Text("Error: Inicia sesión nuevamente.", color=ft.Colors.RED_600))

    user_uid = user_data.get('localId')
    print(f"User UID: {user_uid}")  # Depuración

    # Obtener datos completos del usuario desde la API
    def obtener_datos_usuario():
        try:
            response = api_client.get(f"personas/uid/{user_uid}")
            persona = response[0] if isinstance(response, list) else response
            if persona and 'categoria' in persona:
                return persona
            else:
                raise Exception("Datos de usuario incompletos")
        except Exception as e:
            print(f"Error al obtener datos del usuario: {e}")
            return None

    user_data_complete = obtener_datos_usuario()
    if not user_data_complete:
        page.snack_bar = ft.SnackBar(ft.Text("Error: No se pudieron obtener los datos del usuario."), bgcolor=ft.Colors.RED_600)
        page.snack_bar.open = True
        page.update()
        return ft.Container(content=ft.Text("Error: No se pudieron obtener los datos del usuario.", color=ft.Colors.RED_600))

    user_categoria = user_data_complete.get('categoria')
    print(f"User Categoria: {user_categoria}")  # Depuración

    # Función para mostrar errores
    def show_error_popup(message):
        def close_popup(e):
            page.close(error_dialog)
            page.update()

        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Aceptar", on_click=close_popup)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(error_dialog)
        page.update()

    # Obtener torneos de la categoría del usuario
    def obtener_torneos():
        try:
            response = api_client.get("eventos")
            torneos = [evento for evento in response if evento.get('tipo') == 1 and evento.get('categoria') == user_categoria]
            print(f"Torneos obtenidos: {torneos}")  # Depuración
            return torneos
        except Exception as e:
            show_error_popup(f"Error al obtener torneos: {e}")
            return []

    # Obtener inscripciones del usuario
    def obtener_inscripciones_usuario():
        try:
            response = api_client.get("personasEventos", params={"personaUid": user_uid})
            print(f"Respuesta de la API para inscripciones del usuario: {response}")  # Depuración
            return [inscripcion for inscripcion in response if inscripcion.get('personaUid') == user_uid]
        except Exception as e:
            show_error_popup(f"Error al obtener inscripciones: {e}")
            return []

    # Obtener número de inscritos (solo asistencia: true)
    def obtener_inscritos_autorizados(torneo_id):
        try:
            # Intentar filtrar por asistencia: true en la API
            response = api_client.get("personasEventos", params={"eventoId": torneo_id, "asistencia": "true"})
            print(f"Respuesta de la API para inscritos autorizados (filtrado por asistencia=true): {response}")  # Depuración

            # Filtrado manual como respaldo
            if response:
                inscritos = [inscripcion for inscripcion in response if inscripcion.get('asistencia') in [True, "true"]]
                print(f"Inscritos autorizados después de filtrado manual para torneo {torneo_id}: {inscritos}")  # Depuración
                return len(inscritos)
            else:
                print(f"No se encontraron inscritos para torneo {torneo_id}")
                return 0
        except Exception as e:
            show_error_popup(f"Error al obtener inscritos: {e}")
            return 0

    # Inscribir al usuario en un torneo
    def inscribirse_torneo(torneo_id):
        try:
            # Verificar capacidad (solo inscritos autorizados cuentan)
            inscritos = obtener_inscritos_autorizados(torneo_id)
            torneo = next((t for t in torneos if t['id'] == torneo_id), None)
            if not torneo:
                show_error_popup("Torneo no encontrado.")
                return False

            if inscritos >= torneo['num_personas']:
                show_error_popup("El torneo ha alcanzado su capacidad máxima.")
                return False

            # Inscribir con asistencia: false (en espera)
            response = api_client.post(
                "personasEventos",
                data={"eventoId": torneo_id, "personaUid": user_uid, "asistencia": False}
            )
            print(f"Respuesta de la API al inscribirse: {response}")  # Depuración
            page.snack_bar = ft.SnackBar(ft.Text("Inscripción enviada. Espera autorización del administrador."), bgcolor=ft.Colors.GREEN_600)
            page.snack_bar.open = True
            actualizar_vista()  # Forzar actualización de la vista después de la inscripción
            return True
        except requests.exceptions.HTTPError as e:
            show_error_popup(f"Error al inscribirse: {e.response.status_code}")
            return False
        except Exception as e:
            show_error_popup(f"Error al inscribirse: {e}")
            return False

    # Desinscribirse de un torneo
    def desinscribirse_torneo(inscripcion_id):
        try:
            response = api_client.delete(f"personasEventos/{inscripcion_id}")
            print(f"Respuesta de la API al desinscribirse: {response}")  # Depuración
            page.snack_bar = ft.SnackBar(ft.Text("Te has desinscrito del torneo."), bgcolor=ft.Colors.GREEN_600)
            page.snack_bar.open = True
            actualizar_vista()  # Forzar actualización de la vista después de desinscribirse
            return True
        except requests.exceptions.HTTPError as e:
            show_error_popup(f"Error al desinscribirse: {e.response.status_code}")
            return False
        except Exception as e:
            show_error_popup(f"Error al desinscribirse: {e}")
            return False

    # Crear tarjeta de torneo para el usuario
    def crear_card_torneo(torneo):
        inscripciones = obtener_inscripciones_usuario()
        inscripcion = next((i for i in inscripciones if i['eventoID'] == torneo['id']), None)
        inscritos = obtener_inscritos_autorizados(torneo['id'])

        # Determinar estado y botones
        estado = None
        botones = ft.Row([], alignment=ft.MainAxisAlignment.CENTER)  # Inicialmente vacío

        print(f"Inscripción del usuario para torneo {torneo['id']}: {inscripcion}")  # Depuración

        if inscripcion:
            # Usuario ya está inscrito
            if inscripcion['asistencia'] in [True, "true"]:
                # Autorizado (asistencia: true)
                estado = ft.Text("Admitido: Sí", color=ft.Colors.GREEN_700)
                botones = ft.Row([
                    ft.ElevatedButton(
                        "Desinscribirse",
                        on_click=lambda e: desinscribirse_torneo(inscripcion['id']),
                        bgcolor=ft.Colors.RED_600,
                        color=ft.Colors.WHITE
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            else:
                # En espera de autorización (asistencia: false)
                estado = ft.Text("Admitido: No", color=ft.Colors.ORANGE_700)
                # No mostramos botones (ni "Inscribirse" ni "Desinscribirse")
        else:
            # No inscrito
            botones = ft.Row([
                ft.ElevatedButton(
                    "Inscribirse",
                    on_click=lambda e: inscribirse_torneo(torneo['id']),
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE,
                    disabled=inscritos >= torneo['num_personas']
                )
            ], alignment=ft.MainAxisAlignment.CENTER)

        # Construir tarjeta
        content = [
            ft.Text(torneo["nombre"], size=20, weight="bold", color=ft.Colors.BLUE_900),
            ft.Text(f"Fecha: {torneo['fecha']}", color=ft.Colors.GREY_800),
            ft.Text(f"Hora: {torneo['hora']}", color=ft.Colors.GREY_800),
            ft.Text(f"Categoría: {torneo['categoria']}", color=ft.Colors.GREY_800),
            ft.Text(f"Inscritos: {inscritos}/{torneo['num_personas']}", color=ft.Colors.GREY_800),
        ]
        if estado:
            content.append(estado)
        content.append(botones)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(content, spacing=10),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=8
            ),
            elevation=5,
            width=300
        )

    # Actualizar la vista
    def actualizar_vista():
        grid.controls.clear()
        for torneo in torneos:
            grid.controls.append(crear_card_torneo(torneo))
        page.update()

    # Filtrar torneos por nombre
    def buscar_torneos(e):
        filtro = search_field.value.lower() if search_field.value else ""
        filtered_torneos = [
            torneo for torneo in torneos
            if filtro in torneo["nombre"].lower()
        ]
        grid.controls.clear()
        for torneo in filtered_torneos:
            grid.controls.append(crear_card_torneo(torneo))
        page.update()

    # Inicializar datos
    torneos = obtener_torneos()
    grid = ft.GridView(expand=True, max_extent=300, spacing=20, run_spacing=20, padding=20)
    for torneo in torneos:
        grid.controls.append(crear_card_torneo(torneo))

    # Barra de herramientas
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_600,
        tooltip="Volver",
        on_click=lambda e: page.go("/user_menu")
    )
    search_field = ft.TextField(
        hint_text="Filtrar por nombre de torneo",
        width=300,
        color=ft.Colors.BLACK,
        hint_style=ft.TextStyle(color=ft.Colors.BLACK54),
        border_color=ft.Colors.BLUE_600,
        on_submit=buscar_torneos
    )
    search_icon = ft.IconButton(
        icon=ft.Icons.SEARCH,
        icon_color=ft.Colors.BLUE_600,
        tooltip="Buscar",
        on_click=buscar_torneos
    )
    search_container = ft.Row(
        controls=[
            search_field,
            search_icon
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START
    )
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
        expand=True,
        content=ft.Column([
            toolbar,
            grid
        ]),
        gradient=ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_100]),
        padding=10
    )

User_tournaments = user_tournaments
__all__ = ["User_tournaments"]