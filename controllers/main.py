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

from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

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

PRODUCTOS = {
    "iphone": {
        "nombre": "iPhone 12",
        "precio": "$250.000",
        "descripcion": "iPhone 12 en buen estado.",
        "vendedor": "Estudiante de informática",
    },
    "libro": {
        "nombre": "Libro de cálculo",
        "precio": "$15.000",
        "descripcion": "Libro de cálculo para estudiantes universitarios.",
        "vendedor": "Estudiante de ingeniería",
    },
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

        perfil = self.manager.get_screen("perfil")
        perfil.usuario = usuario
        perfil.actualizar_interfaz()

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
    def on_enter(self, *args):
        self.generar_productos()

    def generar_productos(self):
        contenedor = self.ids.lista_productos
        contenedor.clear_widgets()

        for producto_id, producto in PRODUCTOS.items():
            tarjeta = MDCard(
                style="elevated",
                orientation="vertical",
                padding=dp(15),
                spacing=dp(5),
                size_hint_y=None,
                height=dp(150),
                theme_bg_color="Custom",
                md_bg_color=MDApp.get_running_app().PALETA["blanco"],
            )

            tarjeta.add_widget(
                MDLabel(
                    text=producto["nombre"],
                    font_style="Title",
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["azul_noche"],
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=producto["precio"],
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["primario"],
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=producto["vendedor"],
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["texto_secundario"],
                )
            )

            tarjeta.bind(
                on_release=lambda instancia, pid=producto_id: self.abrir_producto(pid)
            )

            contenedor.add_widget(tarjeta)

    def abrir_producto(self, producto_id):
        pantalla = self.manager.get_screen("producto")
        pantalla.mostrar_producto(producto_id)
        self.manager.current = "producto"

class ProductoScreen(Screen):

    def mostrar_producto(self, producto_id):
        producto = PRODUCTOS[producto_id]

        self.ids.nombre_producto.text = producto["nombre"]
        self.ids.precio_producto.text = producto["precio"]
        self.ids.descripcion_producto.text = producto["descripcion"]
        self.ids.vendedor_producto.text = producto["vendedor"]


class PerfilScreen(Screen):
    usuario = DictProperty({})

    def actualizar_interfaz(self):
        nombre = self.usuario.get("nombre", "")
        self.ids.usuario_nombre_label.text = nombre or "Usuario"
    


class MainApp(MDApp):
    PALETA = DictProperty(PALETA)

    screen_manager = ObjectProperty(None)

    def actualizar_botones_topbar(self, instancia, pantalla):
        botones = self.root.ids.botones_topbar
        en_login = pantalla == "login"

        botones.opacity = 0 if en_login else 1
        botones.disabled = en_login


    def ir_a_pantalla(self, nombre):
        if self.screen_manager and self.screen_manager.has_screen(nombre):
            self.screen_manager.current = nombre

            botones = self.root.ids.botones_topbar
            en_login = nombre == "login"

            botones.opacity = 0 if en_login else 1
            botones.disabled = en_login


    def build(self):
        root = Builder.load_file("views/marketplace.kv")
        self.screen_manager = root.ids.screen_manager

        botones = root.ids.botones_topbar
        en_login = self.screen_manager.current == "login"

        botones.opacity = 0 if en_login else 1
        botones.disabled = en_login

        self.screen_manager.bind(
            current=self.actualizar_botones_topbar
        )

        return root

if __name__ == "__main__":
    MainApp().run()
