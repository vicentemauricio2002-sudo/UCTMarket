import sys
from pathlib import Path

# Añade la raíz del proyecto al path de Python para que reconozca 'models'
sys.path.append(str(Path(__file__).resolve().parent.parent))

from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from models.json_service import get_or_create_user, save_user
from models.notification_service import show_notification
from models.remote_config import get_welcome_message

from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex("#F8FAFC")

def hex_a_rgba(hex_color):
    """Convierte un color HEX (#RRGGBB) a una tupla RGBA para Kivy."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError("El color debe tener el formato #RRGGBB")
    red = int(hex_color[0:2], 16) / 255
    green = int(hex_color[2:4], 16) / 255
    blue = int(hex_color[4:6], 16) / 255
    return (red, green, blue, 1)


PALETA = {
    "azul_noche": hex_a_rgba("#0D1B2A"),
    "azul_oscuro": hex_a_rgba("#1B263B"),
    "azul_intenso": hex_a_rgba("#1D4ED8"),
    "primario": hex_a_rgba("#2563EB"),
    "azul_brillante": hex_a_rgba("#3B82F6"),
    "azul_suave": hex_a_rgba("#93C5FD"),
    "azul_claro": hex_a_rgba("#DBEAFE"),
    "fondo": hex_a_rgba("#F8FAFC"),
    "blanco": hex_a_rgba("#FFFFFF"),
    "texto": hex_a_rgba("#1E293B"),
    "texto_secundario": hex_a_rgba("#475569"),
    "borde": hex_a_rgba("#CBD5E1"),
}


class LoginScreen(Screen):
    def ingresar(self):
        nombre = self.ids.nombre.text.strip()
        if not nombre:
            self.ids.mensaje.text = "Ingresa tu nombre para continuar."
            return

        usuario = get_or_create_user(nombre)
        principal = self.manager.get_screen("principal")
        principal.usuario = usuario
        principal.actualizar_interfaz()

        show_notification(
            "UCTMarket", "Inicio de sesión realizado correctamente."
        )
        self.manager.current = "principal"

    def limpiar_mensaje(self):
        self.ids.mensaje.text = ""


class PrincipalScreen(Screen):
    usuario = DictProperty({})
    bienvenida = StringProperty("Bienvenido a UCTMarket")

    def actualizar_interfaz(self):
        mensaje = get_welcome_message() or "Bienvenido a UCTMarket"
        self.bienvenida = mensaje
        nombre = self.usuario.get("nombre", "")
        self.ids.usuario_label.text = f"{self.bienvenida}, {nombre}"
        self.actualizar_tareas()

    def agregar_tarea(self):
        texto = self.ids.tarea_input.text.strip()
        if not texto:
            return

        self.usuario.setdefault("tareas", []).append(texto)
        save_user(self.usuario)
        self.ids.tarea_input.text = ""
        self.actualizar_tareas()
        show_notification("UCTMarket", "La tarea se guardó correctamente en JSON.")

    def actualizar_tareas(self):
        tareas = self.usuario.get("tareas", [])
        if tareas:
            self.ids.tareas_label.text = "\n".join(f"• {tarea}" for tarea in tareas)
        else:
            self.ids.tareas_label.text = "No hay tareas guardadas."

class MarketScreen(Screen):
    def volver(self):
        self.manager.current = "principal"

class PerfilScreen(Screen):
    def volver(self):
        self.manager.current = "principal"


class MainApp(MDApp):
    PALETA = DictProperty(PALETA)

    screen_manager = ObjectProperty(None)

    def ir_a_pantalla(self, nombre):
        if self.screen_manager and self.screen_manager.has_screen(nombre):
            self.screen_manager.current = nombre

    def build(self):
        root = Builder.load_file("views/marketplace.kv")
        self.screen_manager = root.ids.screen_manager
        return root


if __name__ == "__main__":
    MainApp().run()
