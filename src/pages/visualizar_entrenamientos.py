import flet as ft
from utils.ConexionDB import api_client
from utils.global_state import auth_state

def visualizar_entrenamientos(page: ft.Page):
    user_id = auth_state.user.get("localId") if auth_state.user else None
    if not user_id:
        page.go("/login")
        return ft.Container()

    # Función para crear tarjeta de entrenamiento
    def crear_card_entrenamiento(entrenamiento):
        profesor_id = entrenamiento.get('profesorID')
        profesor = "Desconocido"
        if profesor_id:
            profesor = obtener_nombre_profesor_por_id(profesor_id)
        hora_final = entrenamiento.get('horaFinal', 'No definida')
        
        # Obtener el estado de asistencia para este usuario y evento
        asistencia = obtener_asistencia_entrenamiento(entrenamiento.get('id'))
        asistencia_texto = ft.Text(f"Asistencia: {'Sí' if asistencia else 'No'}", color=ft.Colors.GREEN_700 if asistencia else ft.Colors.RED_700)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(entrenamiento["nombre"], size=20, weight="bold"),
                        ft.Text(f"Fecha: {entrenamiento['fecha']}"),
                        ft.Text(f"Hora: {entrenamiento['hora']}"),
                        ft.Text(f"Hora final: {hora_final}"),
                        ft.Text(f"Categoría: {entrenamiento['categoria']}"),
                        ft.Text(f"Profesor: {profesor}"),
                        asistencia_texto,  # Añadir texto de asistencia
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12)
            ),
            elevation=3,
            width=300
        )

    # Función para obtener el nombre del profesor usando el profesorID
    def obtener_nombre_profesor_por_id(profesor_id):
        try:
            response = api_client.get(f"personas/{profesor_id}")
            if response:
                return response.get('nombre', 'Desconocido')
            return "Desconocido"
        except Exception as e:
            print(f"Error al obtener el profesor: {e}")
            return "Desconocido"

    # Función para obtener el estado de asistencia del usuario en un evento
    def obtener_asistencia_entrenamiento(evento_id):
        try:
            response = api_client.get("personasEventos", params={"eventoId": evento_id, "personaUid": user_id})
            if response and len(response) > 0:
                return response[0].get('asistencia', False) in [True, "true"]
            return False
        except Exception as e:
            print(f"Error al obtener asistencia para evento {evento_id}: {e}")
            return False

    # Función para verificar si el usuario está inscrito en un evento
    def is_user_inscribed(evento_id):
        try:
            response = api_client.get("personasEventos", params={"eventoId": evento_id})
            if not response:
                return False
            return any(item.get("personaUid") == user_id for item in response)
        except Exception as e:
            print(f"Error al verificar inscripción para evento {evento_id}: {e}")
            return False

    # Función para obtener los entrenamientos en los que el usuario está inscrito
    def obtener_entrenamientos_inscritos():
        try:
            print(f"Obteniendo todos los eventos para usuario {user_id}")
            # Obtener todos los eventos
            all_events = api_client.get("eventos") or []

            # Filtrar eventos de tipo 2 y verificar inscripción del usuario
            entrenamientos = []
            for evento in all_events:
                if evento.get('tipo') == 2:
                    if is_user_inscribed(evento.get('id')):
                        entrenamientos.append(evento)
            print(f"Entrenamientos encontrados: {entrenamientos}")
            return entrenamientos
        except Exception as e:
            print(f"Error al obtener los entrenamientos inscritos: {e}")
            return []

    def go_back(page):
        page.go("/user_menu")

    # Cargar los entrenamientos
    entrenamientos_existentes = obtener_entrenamientos_inscritos()

    # Crear las tarjetas
    grid_entrenamientos = ft.GridView(
        expand=True,
        max_extent=250,
        runs_count=3,
        spacing=10,
        run_spacing=10,
    )

    for entrenamiento in entrenamientos_existentes:
        grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))

    # Función de búsqueda
    def buscar_entrenamientos(e):
        filtro = search_field.value.lower()
        filtered_entrenamientos = [
            entrenamiento for entrenamiento in entrenamientos_existentes
            if filtro in entrenamiento["nombre"].lower()
        ]
        grid_entrenamientos.controls.clear()
        for entrenamiento in filtered_entrenamientos:
            grid_entrenamientos.controls.append(crear_card_entrenamiento(entrenamiento))
        page.update()

    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_400,
        icon_size=20,
        tooltip="Volver",
        on_click=lambda e: go_back(page)
    )

    search_field = ft.TextField(
        hint_text="Filtrar por nombre de entrenamiento",
        width=300,
        color=ft.Colors.BLACK,
        hint_style=ft.TextStyle(color=ft.Colors.BLACK54),
    )

    btn_buscar = ft.ElevatedButton("Buscar", on_click=buscar_entrenamientos)

    toolbar_left = ft.Row(
        controls=[btn_volver, search_field, btn_buscar],
        alignment=ft.MainAxisAlignment.START
    )

    toolbar = ft.Row(
        controls=[toolbar_left],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    main_container = ft.Column(
        controls=[toolbar, grid_entrenamientos],
        spacing=10
    )

    visual_container = ft.Container(
        content=main_container,
        gradient=ft.LinearGradient(colors=[ft.Colors.WHITE, ft.Colors.BLUE_200], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
        expand=True,
    )

    return visual_container

Visualizar_entrenamientos = visualizar_entrenamientos

__all__ = ["Visualizar_entrenamientos"]