import sys
from pathlib import Path

# Añade la raíz del proyecto al path de Python para que reconozca 'models'
sys.path.append(str(Path(__file__).resolve().parent.parent))

from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from models.json_service import get_user, create_user, save_user, cargar_productos, guardar_producto
from models.notification_service import show_notification
from models.remote_config import get_welcome_message

from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton
from kivymd.uix.button import MDButtonText
from kivy.uix.modalview import ModalView

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

def formatear_precio(precio):
    return f"${int(precio):,}".replace(",", ".")


class LoginScreen(Screen):
    def ingresar(self):
        nombre = self.ids.nombre.text.strip()
        contrasena = self.ids.contrasena.text
        if not nombre:
            self.ids.mensaje.text = "Ingresa tu nombre para continuar."
            return

        if not contrasena:
            self.ids.mensaje.text = "Ingresa tu contraseña para continuar."
            return

        usuario = get_user(nombre, contrasena)

        if usuario is None:
            self.ids.mensaje.text = "Nombre o contraseña incorrectos."
            return

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


class RegistroScreen(Screen):
    def registrarse(self):
        nombre = self.ids.nombre.text.strip()
        contrasena = self.ids.contrasena.text
        if not nombre:
            self.ids.mensaje.text = "Ingresa tu nombre para continuar."
            return

        if not contrasena:
            self.ids.mensaje.text = "Ingresa tu contraseña para continuar."
            return

        usuario = create_user(nombre, contrasena)

        if usuario is None:
            self.ids.mensaje.text = (
                "Ese nombre ya existe o los datos no son válidos."
            )
            return

        show_notification(
            "UCTMarket", "Registro realizado correctamente."
        )
        self.manager.current = "login"

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

        productos = cargar_productos()

        for producto_id, producto in enumerate(productos, start=1):
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
                    text=formatear_precio(producto["precio"]),
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
        productos = cargar_productos()

        indice = producto_id - 1

        if indice < 0 or indice >= len(productos):
            print("No se encontró el producto:", producto_id)
            return

        producto = productos[indice]

        self.ids.nombre_producto.text = str(producto["nombre"])
        self.ids.precio_producto.text = formatear_precio(producto["precio"])
        self.ids.descripcion_producto.text = str(
            producto.get("descripcion", "Sin descripción")
        )
        self.ids.vendedor_producto.text = str(producto["vendedor"])


class PerfilScreen(Screen):
    usuario = DictProperty({})

    def actualizar_interfaz(self):
        nombre = self.usuario.get("nombre", "")
        self.ids.usuario_nombre_label.text = nombre or "Usuario"
        self.actualizar_publicaciones()

    def actualizar_publicaciones(self):
        nombre_usuario = self.usuario.get("nombre", "").strip()

        if not nombre_usuario:
            self.ids.publicaciones_label.text = (
                "Inicia sesión para ver tus publicaciones."
            )
            return

        productos = cargar_productos()

        mis_productos = [
            producto
            for producto in productos
            if producto.get("vendedor", "").casefold()
            == nombre_usuario.casefold()
        ]

        if not mis_productos:
            self.ids.publicaciones_label.text = (
                "No tienes publicaciones todavía."
            )
            return

        lineas = []

        for producto in mis_productos:
            nombre = producto.get("nombre", "Sin nombre")
            precio = formatear_precio(producto.get("precio", 0))
            descripcion = producto.get(
                "descripcion", "Sin descripción"
            )

            lineas.append(
                f"{nombre} - {precio}\n{descripcion}"
            )

        self.ids.publicaciones_label.text = "\n\n".join(lineas)

    def crear_publicacion(self):
        if not self.usuario.get("nombre"):
            show_notification(
                "UCTMarket",
                "Debes iniciar sesión para publicar productos."
            )
            return

        contenido = MDCard(
            orientation="vertical",
            padding=[dp(20), dp(0), dp(20), dp(20)],
            spacing=dp(10),
            theme_bg_color="Custom",
            md_bg_color=MDApp.get_running_app().PALETA["blanco"],
            radius=[dp(16), dp(16), dp(16), dp(16)],
            elevation=0,
        )

        titulo = MDLabel(
            text="Crear publicación",
            font_style="Headline",
            role="small",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().PALETA["azul_noche"],
            size_hint_y=None,
            height=dp(48),
            halign="left",
            valign="middle",
        )

        nombre_input = MDTextField(
            multiline=False,
            size_hint_y=None,
            height=dp(45),

        )

        nombre_input.add_widget(
            MDTextFieldHintText(
                text="Nombre del producto",
            )
        )

        precio_input = MDTextField(
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(45),

        )

        precio_input.add_widget(
            MDTextFieldHintText(
                text="Precio (ej.: 250000)",
            )
        )

        descripcion_input = MDTextField(
            multiline=True,
            size_hint_y=None,
            height=dp(45),

        )

        descripcion_input.add_widget(
            MDTextFieldHintText(
                text="Descripción del producto",
            )
        )
        

        guardar_boton = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=MDApp.get_running_app().PALETA["primario"],
            size_hint_y=None,
            height=dp(48),
        )

        guardar_boton.add_widget(
            MDButtonText(
                text="Guardar publicación",
                theme_text_color="Custom",
                text_color=MDApp.get_running_app().PALETA["blanco"],
            )
        )

        cancelar_boton = MDButton(
            style="text",
            theme_bg_color="Custom",
            md_bg_color=MDApp.get_running_app().PALETA["azul_suave"],
            size_hint_y=None,
            height=dp(42),
        )

        cancelar_boton.add_widget(
            MDButtonText(
                text="Cancelar",
                theme_text_color="Custom",
                text_color=MDApp.get_running_app().PALETA["primario"],
            )
        )


        modal = ModalView(
            size_hint=(0.85, 0.8),
            auto_dismiss=False,
            background_color=(0, 0, 0, 0),
        )

        guardar_boton.bind(
            on_release=lambda *_: self.guardar_publicacion(
                nombre_input.text,
                precio_input.text,
                descripcion_input.text,
                modal,
            )
        )

        cancelar_boton.bind(
            on_release=lambda *_: modal.dismiss()
        )

        contenido.add_widget(titulo)
        contenido.add_widget(nombre_input)
        contenido.add_widget(precio_input)
        contenido.add_widget(descripcion_input)
        contenido.add_widget(guardar_boton)
        contenido.add_widget(cancelar_boton)

        modal.add_widget(contenido)
        modal.open()

    def guardar_publicacion(
        self, nombre, precio, descripcion, modal
    ):
        nombre = nombre.strip()
        descripcion = descripcion.strip()
        precio = precio.strip()

        if not nombre or not precio or not descripcion:
            show_notification(
                "UCTMarket",
                "Completa todos los campos antes de guardar."
            )
            return

        try:
            precio_numero = int(precio)
        except ValueError:
            show_notification(
                "UCTMarket",
                "El precio debe ser un número entero."
            )
            return

        producto = {
            "nombre": nombre,
            "precio": precio_numero,
            "descripcion": descripcion,
            "vendedor": self.usuario.get("nombre", ""),
        }

        guardado = guardar_producto(producto)

        if not guardado:
            show_notification(
                "UCTMarket",
                "No se pudo guardar la publicación."
            )
            return

        modal.dismiss()
        self.actualizar_publicaciones()

        # Actualiza el catálogo si la pantalla está disponible.
        if self.manager and self.manager.has_screen("market"):
            self.manager.get_screen("market").generar_productos()

        show_notification(
            "UCTMarket",
            "Tu publicación se guardó correctamente."
        )

    


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
