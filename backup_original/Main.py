from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class LoginScreen(MDScreen):

    def ingresar(self):
        nombre = self.ids.nombre.text

        principal = self.manager.get_screen("principal")
        principal.ids.bienvenida.text = f"Bienvenido, {nombre}"

        perfil = self.manager.get_screen("perfil")
        perfil.ids.nombre_perfil.text = nombre

        self.manager.current = "principal"


class PrincipalScreen(MDScreen):
    pass


class PerfilScreen(MDScreen):
    pass


class MarketplaceApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Azure"
        self.theme_cls.theme_style = "Light" 


MarketplaceApp().run()