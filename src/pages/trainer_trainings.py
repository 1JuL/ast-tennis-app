import flet as ft
from utils.ConexionDB import api_client

def trainer_trainings(page: ft.Page):

    # === BACK BUTTON (uses view stack)
    btn_volver = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        tooltip="Volver",
        on_click=lambda e: page.go("/admin_menu"),
    )

    # === FUNCIONES AUXILIARES
    def obtener_estudiantes_por_categoria(categoria):
        try:
            response = api_client.get("personas")
            return [p for p in response if p.get('tipo') == 3 and p.get('categoria') == categoria]
        except Exception as e:
            print(f"Error al obtener estudiantes: {e}")
            return []

    def obtener_estudiantes_inscritos(entrenamiento_id):
        try:
            return api_client.get(f"eventos/{entrenamiento_id}/participantes") or []
        except Exception as e:
            print(f"Error al obtener estudiantes inscritos: {e}")
            return []

    def añadir_estudiante(entrenamiento_id, persona_uid):
        try:
            if api_client.post(f"eventos/{entrenamiento_id}/participantes", data={"personaUid": persona_uid}):
                page.snack_bar = ft.SnackBar(ft.Text("Estudiante añadido"))
                page.snack_bar.open = True
                page.update()
        except Exception as e:
            print(f"Error al añadir estudiante: {e}")
            page.snack_bar = ft.SnackBar(ft.Text("Error al añadir estudiante"))
            page.snack_bar.open = True
            page.update()

    def eliminar_estudiante(entrenamiento_id, persona_uid):
        try:
            if api_client.delete(f"eventos/{entrenamiento_id}/participantes/{persona_uid}"):
                page.snack_bar = ft.SnackBar(ft.Text("Estudiante eliminado"))
                page.snack_bar.open = True
                page.update()
        except Exception as e:
            print(f"Error al eliminar estudiante: {e}")
            page.snack_bar = ft.SnackBar(ft.Text("Error al eliminar estudiante"))
            page.snack_bar.open = True
            page.update()

    def actualizar_asistencia(entrenamiento_id, persona_uid, asistencia):
        try:
            if api_client.put(f"eventos/{entrenamiento_id}/participantes/{persona_uid}", data={"asistencia": asistencia}):
                page.snack_bar = ft.SnackBar(ft.Text("Asistencia actualizada"))
                page.snack_bar.open = True
                page.update()
        except Exception as e:
            print(f"Error al actualizar asistencia: {e}")
            page.snack_bar = ft.SnackBar(ft.Text("Error al actualizar asistencia"))
            page.snack_bar.open = True
            page.update()

    def cerrar_dialogo(dialog):
        dialog.open = False
        page.update()

    def mostrar_dialogo_asistencia(entrenamiento):
        estudiantes = obtener_estudiantes_inscritos(entrenamiento['id'])
        lista = ft.ListView(expand=True)
        for estudiante in estudiantes:
            lista.controls.append(
                ft.ListTile(
                    title=ft.Text(estudiante['persona']['nombre']),
                    trailing=ft.Switch(
                        value=estudiante['asistencia'],
                        on_change=lambda e, uid=estudiante['personaUid']: actualizar_asistencia(
                            entrenamiento['id'], uid, e.control.value
                        )
                    )
                )
            )
        dialog = ft.AlertDialog(
            title=ft.Text(f"Asistencia: {entrenamiento['nombre']}"),
            content=ft.Container(content=lista, height=300, width=400),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialog))]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def abrir_dialogo_añadir(entrenamiento):
        estudiantes_inscritos = obtener_estudiantes_inscritos(entrenamiento['id'])
        estudiantes_disponibles = obtener_estudiantes_por_categoria(entrenamiento['categoria'])
        inscritos_uids = {e['personaUid'] for e in estudiantes_inscritos}
        estudiantes_disponibles = [e for e in estudiantes_disponibles if e['uid'] not in inscritos_uids]

        lista_disponibles = ft.ListView(expand=True)
        for estudiante in estudiantes_disponibles:
            lista_disponibles.controls.append(
                ft.ListTile(
                    title=ft.Text(estudiante['nombre']),
                    trailing=ft.IconButton(
                        icon=ft.icons.ADD,
                        on_click=lambda e, uid=estudiante['uid']: [
                            añadir_estudiante(entrenamiento['id'], uid),
                            actualizar_dialogo_añadir(dialog, entrenamiento)
                        ]
                    )
                )
            )

        lista_inscritos = ft.ListView(expand=True)
        for estudiante in estudiantes_inscritos:
            lista_inscritos.controls.append(
                ft.ListTile(
                    title=ft.Text(estudiante['persona']['nombre']),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, uid=estudiante['personaUid']: [
                            eliminar_estudiante(entrenamiento['id'], uid),
                            actualizar_dialogo_añadir(dialog, entrenamiento)
                        ]
                    )
                )
            )

        contenido = ft.Column([
            ft.Text("Estudiantes Disponibles", weight="bold"),
            ft.Container(content=lista_disponibles, height=200, width=400, border=ft.border.all(1)),
            ft.Text("Estudiantes Inscritos", weight="bold"),
            ft.Container(content=lista_inscritos, height=200, width=400, border=ft.border.all(1))
        ])

        dialog = ft.AlertDialog(
            title=ft.Text(f"Gestionar Estudiantes: {entrenamiento['nombre']}"),
            content=ft.Container(content=contenido, height=450, width=450),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialog))]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def actualizar_dialogo_añadir(dialog, entrenamiento):
        dialog.open = False
        page.update()
        abrir_dialogo_añadir(entrenamiento)

    def obtener_nombre_profesor_por_id(uid):
        try:
            response = api_client.get(f"personas/{uid}")
            return response.get('nombre', 'Desconocido')
        except Exception as e:
            print(f"Error al obtener profesor: {e}")
            return "Desconocido"

    def obtener_entrenamientos_tipo_2():
        try:
            return [e for e in api_client.get("eventos") if e['tipo'] == 2]
        except Exception as e:
            print(f"Error al obtener eventos: {e}")
            return []

    def crear_card_entrenamiento(entrenamiento):
        profesor = obtener_nombre_profesor_por_id(entrenamiento.get('profesorID', ''))
        botones = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Añadir Estudiantes",
                    icon=ft.icons.PERSON_ADD,
                    on_click=lambda e: abrir_dialogo_añadir(entrenamiento),
                    bgcolor=ft.colors.GREEN_400
                ),
                ft.ElevatedButton(
                    "Dar Asistencia",
                    icon=ft.icons.CHECKLIST,
                    on_click=lambda e: mostrar_dialogo_asistencia(entrenamiento),
                    bgcolor=ft.colors.ORANGE_400
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="Volver",
                        width=280,
                        bgcolor="white",
                        on_click=lambda e: page.go("/")
                    ),
                    padding=ft.padding.only(20, 20)
                )
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(entrenamiento['nombre'], size=20, weight="bold"),
                    ft.Text(f"Fecha: {entrenamiento['fecha']}"),
                    ft.Text(f"Categoría: {entrenamiento['categoria']}"),
                    ft.Text(f"Profesor: {profesor}"),
                    botones
                ], spacing=10),
                padding=20,
                bgcolor=ft.colors.WHITE
            ),
            width=300
        )

    # === UI PRINCIPAL ===
    entrenamientos = obtener_entrenamientos_tipo_2()
    grid = ft.GridView(expand=True, max_extent=300, spacing=20, run_spacing=20)
    for e in entrenamientos:
        grid.controls.append(crear_card_entrenamiento(e))

    return ft.Container(
        content=ft.Column([
            ft.Container(
                padding=ft.padding.all(10),
                content=ft.Row(
                    controls=[ft.TextField(hint_text="Buscar entrenamiento...", width=300)],
                    alignment=ft.MainAxisAlignment.START
                )
            ),
            grid
        ]),
        gradient=ft.LinearGradient(colors=[ft.colors.WHITE, ft.colors.BLUE_100]),
        expand=True
    )

Trainer_trainings = trainer_trainings
__all__ = ["trainer_trainings"]
