import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from models.json_service import get_user, create_user, save_user, cargar_productos, guardar_producto, actualizar_producto, eliminar_producto
from models.notification_service import show_notification
from models.remote_config import get_welcome_message

from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton
from kivymd.uix.button import MDButtonText
from kivy.uix.modalview import ModalView
from kivymd.uix.fitimage import FitImage
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDButtonIcon

import uuid

import webbrowser
from urllib.parse import quote

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

        producto = self.manager.get_screen("producto")
        producto.usuario = usuario

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

    def on_enter(self, *args):
        self.mostrar_lista_deseos()

    def actualizar_interfaz(self):
        mensaje = get_welcome_message() or "Bienvenido a UCTMarket"
        self.bienvenida = mensaje
        nombre = self.usuario.get("nombre", "")
        self.ids.usuario_label.text = f"{self.bienvenida}, {nombre}"

    def mostrar_lista_deseos(self):
        contenedor = self.ids.lista_de_deseos_productos
        contenedor.clear_widgets()

        lista_deseos = self.usuario.get("listaDeseos", [])
        if not lista_deseos:
            self.ids.listdeseos_label.text = "Tu lista de deseos está vacía."
            return

        self.ids.listdeseos_label.text = ""

        productos = cargar_productos()
        productos_deseados = [
            p for p in productos if p.get("id") in lista_deseos
        ]

        if not productos_deseados:
            self.ids.listdeseos_label.text = "No se encontraron productos en tu lista de deseos."

        for producto in productos_deseados:
            producto_id = producto["id"]

            tarjeta = MDCard(
                style="filled",
                orientation="vertical",
                padding=dp(15),
                spacing=dp(5),
                size_hint=(None, None),
                theme_bg_color="Custom",
                md_bg_color=MDApp.get_running_app().PALETA["fondo"],
            )

            tarjeta.add_widget(
                FitImage(
                    source=producto.get(
                    "imagen",
                    "imgs/img_productos/placeholder.png"
                ),
                    size_hint_y=0.70
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=producto["nombre"],
                    font_style="Title",
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["azul_noche"],
                    size_hint_y=0.10
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=formatear_precio(producto["precio"]),
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["primario"],
                    size_hint_y=0.10
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=producto["vendedor"],
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["texto_secundario"],
                    size_hint_y=0.10
                )
            )

            tarjeta.bind(
                on_release=lambda instancia, pid=producto_id: self.abrir_producto(pid)
            )

            contenedor.add_widget(tarjeta)
            
        self.ajustar_tamano(contenedor, contenedor.width)
                    
    def abrir_producto(self, producto_id):
        pantalla = self.manager.get_screen("producto")
        pantalla.pantalla_anterior = "principal"
        pantalla.mostrar_producto(producto_id)

        self.manager.current = "producto"

    def ajustar_tamano(self, instancia, ancho):
        ancho_tarjeta = (ancho - dp(16)) / 2

        for tarjeta in instancia.children:
            tarjeta.size = (ancho_tarjeta, ancho_tarjeta)

class MarketScreen(Screen):
    def on_enter(self, *args):
        self.generar_productos()

    def generar_productos(self, productos=None):
        contenedor = self.ids.lista_productos
        contenedor.clear_widgets()

        if productos is None:
            productos = cargar_productos()

        for producto in productos:
            producto_id = producto["id"]

            tarjeta = MDCard(
                style="elevated",
                orientation="vertical",
                padding=dp(15),
                spacing=dp(5),
                size_hint=(None, None),
                theme_bg_color="Custom",
                md_bg_color=MDApp.get_running_app().PALETA["blanco"],
            )
            tarjeta.bind(
                width=lambda instance, value: setattr(instance, 'height', value)
            )

            tarjeta.add_widget(
                FitImage(
                    source=producto.get(
                        "imagen",
                        "imgs/img_productos/placeholder.png"
                    ),
                    size_hint_y=0.70
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=producto["nombre"],
                    font_style="Title",
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["azul_noche"],
                    size_hint_y=0.10
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=formatear_precio(producto["precio"]),
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["primario"],
                    size_hint_y=0.10
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=producto["vendedor"],
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["texto_secundario"],
                    size_hint_y=0.10
                )
            )

            tarjeta.bind(
                on_release=lambda instancia, pid=producto_id: self.abrir_producto(pid)
            )

            contenedor.add_widget(tarjeta)

        self.ajustar_tamano(contenedor, contenedor.width)

    def ajustar_tamano(self, instancia, ancho):
        ancho_tarjeta = (ancho - dp(16)) / 2

        for tarjeta in instancia.children:
            tarjeta.size = (ancho_tarjeta, ancho_tarjeta)

    def abrir_producto(self, producto_id):
        pantalla = self.manager.get_screen("producto")
        pantalla.pantalla_anterior = "market"
        pantalla.mostrar_producto(producto_id)

        self.manager.current = "producto"

    def buscar_productos(self, texto):
        productos = cargar_productos()

        texto = texto.strip().lower()

        if not texto:
            self.generar_productos(productos)
            return

        resultados = [
            producto for producto in productos
            if texto in producto.get("nombre", "").lower()
        ]

        self.generar_productos(resultados)
        

class ProductoScreen(Screen):

    usuario = DictProperty({})
    producto_actual = DictProperty({})
    es_mi_publicacion = BooleanProperty(False)

    pantalla_anterior = StringProperty("market")

    def volver(self):
        self.manager.current = self.pantalla_anterior

    icono_deseos = StringProperty("heart-outline")

    def mostrar_producto(self, producto_id):
        productos = cargar_productos()

        producto = next(
            (p for p in productos if p.get("id") == producto_id),
            None
        )

        if producto is None:
            print("No se encontró el producto:", producto_id)
            return

        self.producto_actual = producto

        lista_deseos = self.usuario.get("listaDeseos", [])
        self.icono_deseos = (
            "heart" if producto_id in lista_deseos
            else "heart-outline"
)
        self.es_mi_publicacion = (
            producto.get("vendedor", "") == self.usuario.get("nombre", "")
        )
        self.producto_id = producto_id

        self.ids.nombre_producto.text = str(producto["nombre"])
        self.ids.imagen_producto.source = producto.get(
            "imagen", "imgs/img_productos/placeholder.png"
        )
        self.ids.precio_producto.text = formatear_precio(producto["precio"])
        self.ids.descripcion_producto.text = str(
            producto.get("descripcion", "Sin descripción")
        )
        self.ids.vendedor_producto.text = str(producto["vendedor"])

    def comprar_producto(self):
        producto = self.producto_actual

        whatsapp = producto.get("whatsapp", "")
        nombre = producto.get("nombre", "este producto")

        if not whatsapp:
            show_notification(
                "Contacto no disponible",
                "El vendedor no ha registrado su WhatsApp."
            )
            return

        mensaje = (
            f"Hola, vi tu publicación de '{nombre}' "
            "en UCTMarket y me interesa. ¿Sigue disponible?"
        )

        enlace = f"https://wa.me/{whatsapp}?text={quote(mensaje)}"

        webbrowser.open(enlace)
        
    def ver_imagen_completa(self):
        imagen_path = self.ids.imagen_producto.source
        if not imagen_path or imagen_path == "imgs/img_productos/placeholder.png":
            return

        modal = ModalView(size_hint=(0.9, 0.9))
        fit_image = FitImage(source=imagen_path, allow_stretch=True)
        modal.add_widget(fit_image)
        modal.open()

    def editar_publicacion(self):
        producto = self.producto_actual

        modal = ModalView(
            size_hint=(0.85, 0.85),
            background="",
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.5),
        )

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(4),
        )

        contenedor = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            size_hint_y=None,
            padding=dp(10),
        )
        
        contenido = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            padding=[dp(24), dp(24), dp(24), dp(24)],
            size_hint_y=None,
            adaptive_height=True,
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(20)],
        )

        titulo = MDLabel(
            text="Editar publicación",
            font_style="Headline",
            role="medium",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().PALETA["azul_noche"],
            adaptive_height=True,
        )

        nombre = MDTextField(
            mode="outlined",
            multiline=False,
            text=str(producto.get("nombre", "")),
        )
        nombre.add_widget(MDTextFieldHintText(text="Nombre del producto"))

        vista_previa = FitImage(
            source=producto.get(
                "imagen", "imgs/img_productos/placeholder.png"
            ),
            size_hint=(1, None),
            height=dp(180),
        )

        ruta_imagen = {"path": producto.get("imagen", None)}

        def seleccionar_imagen(*args):
            selector = FileChooserListView(
                path=str(Path.home()),
                filters=["*.png", "*.jpg", "*.jpeg", "*.webp"],
            )

            def colorear_entrada(chooser, entrada, parent):
                for widget in entrada.walk():
                    if isinstance(widget, Label):
                        widget.color = MDApp.get_running_app().PALETA["azul_noche"]

            selector.bind(on_entry_added=colorear_entrada)

            selector_modal = ModalView(
                size_hint=(0.9, 0.85),
                background="",
                overlay_color=(0, 0, 0, 0.5),
            )

            selector_contenido = MDBoxLayout(
                orientation="vertical",
                padding=dp(12),
                spacing=dp(10),
            )

            boton_usar = MDButton(style="filled")
            boton_usar.add_widget(MDButtonText(text="Usar imagen"))

            def confirmar_imagen(*args):
                if not selector.selection:
                    return

                ruta = selector.selection[0]

                ruta_imagen["path"] = ruta
                vista_previa.source = ruta

                selector_modal.dismiss()

            boton_usar.bind(on_release=confirmar_imagen)

            selector_contenido.add_widget(selector)
            selector_contenido.add_widget(boton_usar)

            selector_modal.add_widget(selector_contenido)
            selector_modal.open()

        seleccionar = MDButton(style="text")
        
        seleccionar.add_widget(
            MDButtonIcon(icon="image-outline")
        )

        seleccionar.add_widget(
            MDButtonText(text="Seleccionar imagen")
        )

        seleccionar.bind(on_release=seleccionar_imagen)

        precio = MDTextField(
            mode="outlined",
            multiline=False,
            input_filter="int",
            text=str(producto.get("precio", "")),
        )
        precio.add_widget(MDTextFieldHintText(text="Precio"))

        descripcion = MDTextField(
            mode="outlined",
            multiline=True,
            text=str(producto.get("descripcion", ""))
        )
        descripcion.add_widget(
            MDTextFieldHintText(text="Descripción del producto")
        )

        contacto = MDTextField(
            mode="outlined",
            multiline=False,
            input_filter="int",
            text=str(producto.get("whatsapp", "")),
        )
        contacto.add_widget(
            MDTextFieldHintText(text="WhatsApp (Ej: 56912345678)")
        )

        botones = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            spacing=dp(12),
        )

        cancelar = MDButton(style="outlined")
        cancelar.add_widget(MDButtonText(text="Cancelar"))
        cancelar.bind(on_release=lambda *args: modal.dismiss())

        guardar = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=MDApp.get_running_app().PALETA["primario"],
            on_release=lambda *args: self.guardar_edicion(
                nombre.text,
                precio.text,
                descripcion.text,
                contacto.text,
                ruta_imagen["path"],
                modal
            )
        )
        guardar.add_widget(
            MDButtonText(
                text="Guardar",
                theme_text_color="Custom",
                text_color=MDApp.get_running_app().PALETA["blanco"],
            )
        )

        eliminar = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0.85, 0.15, 0.15, 1),
        )

        eliminar.add_widget(
            MDButtonText(
                text="Eliminar",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
            )
        )

        eliminar.bind(
            on_release=lambda *args: self.eliminar_publicacion(modal)
        )

        botones.add_widget(eliminar)
        botones.add_widget(cancelar)
        botones.add_widget(guardar)

        contenido.add_widget(titulo)
        contenido.add_widget(nombre)
        contenido.add_widget(precio)
        contenido.add_widget(descripcion)
        contenido.add_widget(contacto)
        contenido.add_widget(vista_previa)
        contenido.add_widget(seleccionar)
        contenido.add_widget(botones)

        contenedor.add_widget(contenido)
        scroll.add_widget(contenedor)
        modal.add_widget(scroll)

        modal.open()

    def guardar_edicion(self, nombre, precio, descripcion, contacto, ruta_imagen, modal):
        nombre = nombre.strip()
        descripcion = descripcion.strip()

        if not nombre or not precio or not descripcion:
            show_notification(
                "Datos incompletos",
                "Debes completar todos los campos."
            )
            return

        try:
            precio = int(precio)

            if precio <= 0:
                raise ValueError

        except (ValueError, TypeError):
            show_notification(
                "Precio inválido",
                "Ingresa un precio mayor que cero."
            )
            return

        contacto = contacto.strip()

        if not contacto.startswith("569") or len(contacto) != 11:
            show_notification(
                "WhatsApp inválido",
                "Ingresa un número chileno válido. Ejemplo: 56912345678."
            )
            return

        # Mantener los datos originales de la publicación.
        producto = self.producto_actual.copy()

        # Actualizar los campos editables.
        producto["nombre"] = nombre
        producto["precio"] = precio
        producto["descripcion"] = descripcion
        producto["whatsapp"] = contacto

        # Mantener la imagen actual si no se seleccionó otra.
        imagen_original = self.producto_actual.get(
            "imagen",
            "imgs/img_productos/placeholder.png"
        )

        imagen = imagen_original

        if ruta_imagen and ruta_imagen != imagen_original:
            import shutil

            try:
                origen = Path(ruta_imagen)

                carpeta = (
                    Path(__file__).resolve().parent.parent
                    / "imgs"
                    / "img_productos"
                )
                carpeta.mkdir(parents=True, exist_ok=True)

                nombre_imagen = f"{uuid.uuid4().hex}{origen.suffix.lower()}"
                destino = carpeta / nombre_imagen

                shutil.copy2(origen, destino)

                imagen = f"imgs/img_productos/{nombre_imagen}"

            except OSError as error:
                print("Error al copiar la imagen:", error)

                show_notification(
                    "Error con la imagen",
                    "No se pudo guardar la imagen seleccionada."
                )
                return

        producto["imagen"] = imagen

        # Actualizar el producto existente en el JSON.
        resultado = actualizar_producto(self.producto_id, producto)

        if resultado:
            self.producto_actual = producto

            # Actualizar la información visible.
            self.ids.nombre_producto.text = producto["nombre"]
            self.ids.precio_producto.text = formatear_precio(producto["precio"])
            self.ids.descripcion_producto.text = producto["descripcion"]
            self.ids.imagen_producto.source = producto["imagen"]

            show_notification(
                "Publicación actualizada",
                f"Tu producto '{nombre}' se actualizó correctamente."
            )

            modal.dismiss()

            # Actualizar la pantalla desde la que se abrió el producto.
            if self.pantalla_anterior == "perfil":
                perfil = self.manager.get_screen("perfil")
                perfil.mostrar_tus_publicaciones()

            elif self.pantalla_anterior == "market":
                market = self.manager.get_screen("market")
                market.generar_productos()

        else:
            show_notification(
                "Error al actualizar",
                "No se pudieron guardar los cambios."
            )
    
    def eliminar_publicacion(self, modal_edicion):
        confirmacion = ModalView(
            size_hint=(0.75, None),
            height=dp(190),
            background="",
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.5),
        )

        contenido = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            md_bg_color=MDApp.get_running_app().PALETA["blanco"],
            radius=[dp(20)],
        )

        titulo = MDLabel(
            text="¿Eliminar publicación?",
            font_style="Title",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().PALETA["azul_noche"],
            adaptive_height=True,
        )

        mensaje = MDLabel(
            text="Esta acción no se puede deshacer.",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().PALETA["texto_secundario"],
            adaptive_height=True,
        )

        botones = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            spacing=dp(10),
        )

        cancelar = MDButton(style="outlined")
        cancelar.add_widget(MDButtonText(text="Cancelar"))
        cancelar.bind(
            on_release=lambda *args: confirmacion.dismiss()
        )

        eliminar = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0.85, 0.15, 0.15, 1),
        )

        eliminar.add_widget(
            MDButtonText(
                text="Eliminar",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
            )
        )

        def confirmar_eliminacion(*args):
            resultado = eliminar_producto(self.producto_id)

            if resultado:
                show_notification(
                    "Publicación eliminada",
                    "Tu publicación se eliminó correctamente."
                )

                confirmacion.dismiss()
                modal_edicion.dismiss()

                if self.pantalla_anterior == "perfil":
                    perfil = self.manager.get_screen("perfil")
                    perfil.mostrar_tus_publicaciones()

                elif self.pantalla_anterior == "market":
                    market = self.manager.get_screen("market")
                    market.generar_productos()

                self.volver()

            else:
                show_notification(
                    "Error al eliminar",
                    "No se pudo eliminar la publicación."
                )

        eliminar.bind(on_release=confirmar_eliminacion)

        botones.add_widget(cancelar)
        botones.add_widget(eliminar)

        contenido.add_widget(titulo)
        contenido.add_widget(mensaje)
        contenido.add_widget(botones)

        confirmacion.add_widget(contenido)
        confirmacion.open()

    def alternar_lista_deseos(self):
        producto = self.producto_actual
        usuario = self.usuario

        if not producto or not usuario:
            return

        producto_id = producto["id"]
        lista_deseos = usuario.get("listaDeseos", [])

        # Comprobar si el producto ya está en la lista
        if producto_id in lista_deseos:
            lista_deseos.remove(producto_id)
            nuevo_icono = "heart-outline"
            mensaje = "Producto eliminado de tu lista de deseos."

        else:
            lista_deseos.append(producto_id)
            nuevo_icono = "heart"
            mensaje = "Producto agregado a tu lista de deseos."

        usuario["listaDeseos"] = lista_deseos

        resultado = save_user(usuario)

        if resultado:
            self.icono_deseos = nuevo_icono
            show_notification("Lista de deseos", mensaje)

        else:
            show_notification(
                "Error",
                "No se pudo actualizar tu lista de deseos."
            )




class PerfilScreen(Screen):
    usuario = DictProperty({})

    def on_kv_post(self, base_widget):
        contenedor = self.ids.lista_perfil_productos
        contenedor.bind(width=self.ajustar_tamano)

    def ajustar_tamano(self, instancia, ancho):
        ancho_tarjeta = (ancho - dp(16)) / 2

        for tarjeta in instancia.children:
            tarjeta.size = (ancho_tarjeta, ancho_tarjeta)

    def on_enter(self, *args):
        self.actualizar_interfaz()
        self.actualizar_foto_perfil()
        self.mostrar_tus_publicaciones()

    def actualizar_interfaz(self):
        nombre = self.usuario.get("nombre", "")
        self.ids.usuario_nombre_label.text = nombre or "Usuario"

    def actualizar_foto_perfil(self):
        foto_path = self.usuario.get("usuarioFoto", "")
        if foto_path:
            self.ids.usuario_foto.source = foto_path
        else:
            self.ids.usuario_foto.source = "imgs/img_perfiles/placeholder.png"

    def crear_publicacion(self):
        modal = ModalView(
            size_hint=(0.85, 0.85),
            background="",
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.5),
        )

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(4),
        )

        contenedor = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            size_hint_y=None,
            padding=dp(10),
        )
        
        contenido = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            padding=[dp(24), dp(24), dp(24), dp(24)],
            size_hint_y=None,
            adaptive_height=True,
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(20)],
        )

        titulo = MDLabel(
            text="Crear publicación",
            font_style="Headline",
            role="medium",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().PALETA["azul_noche"],
            adaptive_height=True,
        )

        nombre = MDTextField(
            mode="outlined",
            multiline=False,
        )
        nombre.add_widget(MDTextFieldHintText(text="Nombre del producto (Ej: Celular, Laptop, etc.)"))

        precio = MDTextField(
            mode="outlined",
            multiline=False,
            input_filter="int",
        )
        precio.add_widget(MDTextFieldHintText(text="Precio (Ej: 1000, 20000, etc.)"))

        descripcion = MDTextField(
            mode="outlined",
            multiline=True,
        )
        descripcion.add_widget(
            MDTextFieldHintText(text="Descripción del producto (Ej: Excelente estado, sin uso, etc.)")
        )

        contacto = MDTextField(
            mode="outlined",
            multiline=False,
            input_filter="int",
        )
        contacto.add_widget(
            MDTextFieldHintText(text="WhatsApp (Ej: 56912345678)")
        )

        vista_previa = FitImage(
            source="imgs/img_productos/placeholder.png",
            size_hint=(1, None),
            height=dp(180),
        )

        ruta_imagen = {"path": None}

        def seleccionar_imagen(*args):
            selector = FileChooserListView(
                path=str(Path.home()),
                filters=["*.png", "*.jpg", "*.jpeg", "*.webp"],
            )

            def colorear_entrada(chooser, entrada, parent):
                for widget in entrada.walk():
                    if isinstance(widget, Label):
                        widget.color = MDApp.get_running_app().PALETA["azul_noche"]

            selector.bind(on_entry_added=colorear_entrada)

            selector_modal = ModalView(
                size_hint=(0.9, 0.85),
                background="",
                overlay_color=(0, 0, 0, 0.5),
            )

            selector_contenido = MDBoxLayout(
                orientation="vertical",
                padding=dp(12),
                spacing=dp(10),
            )

            boton_usar = MDButton(style="filled")
            boton_usar.add_widget(MDButtonText(text="Usar imagen"))

            def confirmar_imagen(*args):
                if not selector.selection:
                    return

                ruta = selector.selection[0]

                ruta_imagen["path"] = ruta
                vista_previa.source = ruta

                selector_modal.dismiss()

            boton_usar.bind(on_release=confirmar_imagen)

            selector_contenido.add_widget(selector)
            selector_contenido.add_widget(boton_usar)

            selector_modal.add_widget(selector_contenido)
            selector_modal.open()

        seleccionar = MDButton(style="text")
                
        seleccionar.add_widget(
            MDButtonIcon(icon="image-outline")
        )

        seleccionar.add_widget(
            MDButtonText(text="Seleccionar imagen")
        )
        


        seleccionar.bind(on_release=seleccionar_imagen)

        botones = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            spacing=dp(12),
        )

        cancelar = MDButton(style="outlined")
        cancelar.add_widget(MDButtonText(text="Cancelar"))
        cancelar.bind(on_release=lambda *args: modal.dismiss())

        publicar = MDButton(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=MDApp.get_running_app().PALETA["primario"],
            on_release=lambda *args: self.guardar_publicacion(
                nombre.text,
                precio.text,
                descripcion.text,
                contacto.text,
                ruta_imagen["path"],
                modal
            )
        )
        publicar.add_widget(
            MDButtonText(
                text="Publicar",
                theme_text_color="Custom",
                text_color=MDApp.get_running_app().PALETA["blanco"],
            )
        )

        botones.add_widget(cancelar)
        botones.add_widget(publicar)

        contenido.add_widget(titulo)
        contenido.add_widget(nombre)
        contenido.add_widget(precio)
        contenido.add_widget(descripcion)
        contenido.add_widget(contacto)
        contenido.add_widget(vista_previa)
        contenido.add_widget(seleccionar)
        contenido.add_widget(botones)

        contenedor.add_widget(contenido)
        scroll.add_widget(contenedor)
        modal.add_widget(scroll)

        modal.open()
    
    def guardar_publicacion(self, nombre, precio, descripcion, contacto, ruta_imagen, modal):
        nombre = nombre.strip()
        descripcion = descripcion.strip()
        vendedor = self.usuario.get("nombre", "")

        # Validar campos
        if not nombre or not precio or not descripcion:
            show_notification(
                "Datos incompletos",
                "Debes completar todos los campos."
            )
            return

        # Validar precio
        try:
            precio = int(precio)

            if precio <= 0:
                raise ValueError

        except (ValueError, TypeError):
            show_notification(
                "Precio inválido",
                "Ingresa un precio mayor que cero."
            )
            return

        contacto = contacto.strip()

        if not contacto.startswith("569") or len(contacto) != 11:
            show_notification(
                "WhatsApp inválido",
                "Ingresa un número chileno válido. Ejemplo: 56912345678."
            )
            return

        # Preparar imagen
        imagen = "imgs/img_productos/placeholder.png"

        if ruta_imagen:
            import shutil

            try:
                origen = Path(ruta_imagen)

                carpeta = Path(__file__).resolve().parent.parent / "imgs" / "img_productos"
                carpeta.mkdir(parents=True, exist_ok=True)

                nombre_imagen = f"{uuid.uuid4().hex}{origen.suffix.lower()}"
                destino = carpeta / nombre_imagen

                shutil.copy2(origen, destino)

                imagen = f"imgs/img_productos/{nombre_imagen}"

            except OSError as error:
                print("Error al copiar la imagen:", error)

                show_notification(
                    "Error con la imagen",
                    "No se pudo guardar la imagen seleccionada."
                )
                return

        # Crear diccionario del producto
        producto = {
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "precio": precio,
            "descripcion": descripcion,
            "vendedor": vendedor,
            "whatsapp": contacto,
            "imagen": imagen
        }

        # Guardar publicación en JSON
        resultado = guardar_producto(producto)

        if resultado:
            show_notification(
                "Publicación creada",
                f"Tu producto '{nombre}' se publicó correctamente."
            )

            modal.dismiss()
            self.mostrar_tus_publicaciones()

        else:
            show_notification(
                "Error al publicar",
                "No se pudo guardar tu publicación."
            )
    
    def mostrar_tus_publicaciones(self):
        contenedor = self.ids.lista_perfil_productos
        contenedor.clear_widgets()
        productos = cargar_productos()

        for producto in productos:
            producto_id = producto["id"]

            if producto.get("vendedor", "") != self.usuario.get("nombre", ""):
                continue

            tarjeta = MDCard(
                style="filled",
                orientation="vertical",
                padding=dp(15),
                spacing=dp(5),
                size_hint=(None, None),
                theme_bg_color="Custom",
                md_bg_color=MDApp.get_running_app().PALETA["fondo"],
            )

            tarjeta.add_widget(
                FitImage(
                    source=producto.get(
                    "imagen",
                    "imgs/img_productos/placeholder.png"
                ),
                    size_hint_y=0.70
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=producto["nombre"],
                    font_style="Title",
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["azul_noche"],
                    size_hint_y=0.10
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=formatear_precio(producto["precio"]),
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["primario"],
                    size_hint_y=0.10
                )
            )

            tarjeta.add_widget(
                MDLabel(
                    text=producto["vendedor"],
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().PALETA["texto_secundario"],
                    size_hint_y=0.10
                )
            )

            tarjeta.bind(
                on_release=lambda instancia, pid=producto_id: self.abrir_producto(pid)
            )

            contenedor.add_widget(tarjeta)
        self.ajustar_tamano(contenedor, contenedor.width)
        
    def abrir_producto(self, producto_id):
        pantalla = self.manager.get_screen("producto")
        pantalla.pantalla_anterior = "perfil"
        pantalla.mostrar_producto(producto_id)

        self.manager.current = "producto"


class MainApp(MDApp):
    PALETA = DictProperty(PALETA)

    screen_manager = ObjectProperty(None)

    def actualizar_botones_topbar(self, instancia, pantalla):
        botones = self.root.ids.botones_topbar
        en_login = pantalla in ["login", "registro"]

        botones.opacity = 0 if en_login else 1
        botones.disabled = True if en_login else False


    def ir_a_pantalla(self, nombre):
        if self.screen_manager and self.screen_manager.has_screen(nombre):
            self.screen_manager.current = nombre

            botones = self.root.ids.botones_topbar
            en_login = nombre in ["login", "registro"]

            botones.opacity = 0 if en_login else 1
            botones.disabled = True if en_login else False


    def build(self):
        root = Builder.load_file("views/marketplace.kv")
        self.screen_manager = root.ids.screen_manager

        botones = root.ids.botones_topbar
        en_login = self.screen_manager.current in ["login", "registro"]

        botones.opacity = 0 if en_login else 1
        botones.disabled = True if en_login else False

        self.screen_manager.bind(
            current=self.actualizar_botones_topbar
        )

        return root

if __name__ == "__main__":
    MainApp().run()
