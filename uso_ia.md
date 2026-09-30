te explicare el contexto estamos haciendo una aplicación Marketplace (como el de Facebook) para la UCT, ahora mismo necesitamos crear el diseño de esta app usando kivy aplicando todo lo que hemos hecho en los ejercicios anteriores aquí están las instrucciones y rubrica de evaluación, solo necesitamos el diseño de la aplicación no es necesario que tenga funciones activas 

Perfecto. Ahora que veo la rúbrica completa, cambia un poco el enfoque: ya no estamos haciendo ejercicios aislados, sino la maqueta de la aplicación Marketplace para la UCT. Y sí, podemos reutilizar prácticamente todo lo aprendido: .py, .kv, ScreenManager, get_screen(), MDTextField, MDLabel, MDButton, MDCard, etc.

La rúbrica deja bastante claro qué debemos construir. La evaluación exige una app ejecutable con mínimo 3 pantallas, navegación con ScreenManager, separación .py/.kv y componentes KivyMD.

🎯 Qué vamos a construir

Yo propondría inicialmente estas 3 pantallas principales:

                    ┌──────────────┐
                    │   LOGIN      │
                    │              │
                    │ Nombre       │
                    │ [_________]  │
                    │              │
                    │ [ INGRESAR ] │
                    └──────┬───────┘
                           │
                           ▼
                ┌─────────────────────┐
                │      MARKETPLACE    │
                │                     │
                │ Buscar productos... │
                │                     │
                │ ┌──────┐ ┌──────┐  │
                │ │Venta │ │Venta │  │
                │ │ ...  │ │ ...  │  │
                │ └──────┘ └──────┘  │
                │                     │
                │ Inicio  Perfil      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │       PERFIL        │
                │                     │
                │       👤            │
                │                     │
                │ Nombre estudiante   │
                │                     │
                │ [Mis publicaciones] │
                │ [Volver]            │
                └─────────────────────┘

Esto además encaja muy bien con lo que hemos estado practicando.

1. main.py

Aquí pondremos la lógica, no el diseño.

Por ejemplo:

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):

    def ingresar(self):
        nombre = self.ids.nombre.text

        principal = self.manager.get_screen("principal")
        principal.ids.bienvenida.text = f"Bienvenido, {nombre}"

        perfil = self.manager.get_screen("perfil")
        perfil.ids.nombre_perfil.text = nombre

        self.manager.current = "principal"


class PrincipalScreen(Screen):
    pass


class PerfilScreen(Screen):
    pass


class MarketplaceApp(MDApp):
    pass


MarketplaceApp().run()

Fíjate que estamos reutilizando exactamente lo que aprendiste:

nombre = self.ids.nombre.text

↓

self.manager.get_screen("principal")

↓

principal.ids.bienvenida.text = ...

↓

self.manager.current = "principal"

Eso demuestra el uso de ids, root/manager, get_screen() y ScreenManager.

2. marketplace.kv

Aquí estará todo el diseño visual.

La primera parte será nuestro ScreenManager:

ScreenManager:

    LoginScreen:
        name: "login"

    PrincipalScreen:
        name: "principal"

    PerfilScreen:
        name: "perfil"

Y después diseñaremos cada pantalla.

Login

Usaremos:

MDLabel
MDTextField
MDButton
<LoginScreen>:

    MDBoxLayout:
        orientation: "vertical"
        padding: "40dp"
        spacing: "25dp"

        MDLabel:
            text: "Marketplace UCT"
            halign: "center"
            font_style: "Headline"

        MDLabel:
            text: "Compra, vende e intercambia dentro de la comunidad universitaria"
            halign: "center"

        MDTextField:
            id: nombre
            hint_text: "Ingresa tu nombre"
            mode: "outlined"

        MDRaisedButton:
            text: "Ingresar"
            pos_hint: {"center_x": 0.5}
            on_release: root.ingresar()
3. Pantalla principal

Aquí es donde la aplicación empieza a parecer realmente un Marketplace.

Podemos colocar:

Marketplace UCT

[ 🔎 Buscar productos...]

Publicaciones recientes

┌──────────────────┐
│ 📱              │
│ iPhone 12        │
│ $250.000         │
│ Estudiante UCT   │
└──────────────────┘

┌──────────────────┐
│ 📚              │
│ Libros de cálculo│
│ $15.000          │
│ Estudiante UCT   │
└──────────────────┘

             [Inicio] [Perfil]

Para eso podemos utilizar MDCard, que la propia rúbrica menciona como uno de los componentes KivyMD esperados.

Por ejemplo:

<PrincipalScreen>:

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Marketplace UCT"

        MDTextField:
            hint_text: "Buscar productos..."
            mode: "outlined"
            size_hint_y: None
            height: "60dp"

        MDLabel:
            text: "Publicaciones recientes"
            font_style: "Title"
            padding: "20dp", "10dp"

        MDCard:
            orientation: "vertical"
            padding: "15dp"
            size_hint_y: None
            height: "180dp"

            MDLabel:
                text: "📱 iPhone 12"
                font_style: "Title"

            MDLabel:
                text: "$250.000"

            MDLabel:
                text: "Publicado por estudiante UCT"

        MDCard:
            orientation: "vertical"
            padding: "15dp"
            size_hint_y: None
            height: "180dp"

            MDLabel:
                text: "📚 Libros de cálculo"
                font_style: "Title"

            MDLabel:
                text: "$15.000"

            MDLabel:
                text: "Publicado por estudiante UCT"

        Widget:

        MDButton:
            text: "Ver perfil"
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = "perfil"
4. Perfil

La tercera pantalla:

<PerfilScreen>:

    MDBoxLayout:
        orientation: "vertical"
        padding: "30dp"
        spacing: "20dp"

        MDTopAppBar:
            title: "Mi perfil"

        MDLabel:
            text: "👤"
            halign: "center"
            font_size: "60sp"

        MDLabel:
            id: nombre_perfil
            text: "Usuario"
            halign: "center"
            font_style: "Headline"

        MDButton:
            text: "Mis publicaciones"
            pos_hint: {"center_x": 0.5}

        MDButton:
            text: "Volver al Marketplace"
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = "principal"
⚠️ Pero hay algo MUY importante de la rúbrica

Aunque me dices que no necesitamos funciones activas, hay que distinguir entre:

❌ Funciones que NO necesitamos

No necesitamos implementar todavía:

Base de datos.
Comprar realmente.
Publicar realmente.
Sistema de usuarios.
Autenticación.
Persistencia.
Notificaciones.

De hecho, la rúbrica dice explícitamente que persistencia, autenticación, notificaciones y configuración remota están fuera de alcance y no son necesarias para esta evaluación.

✅ Funciones que SÍ conviene que funcionen

Para no perder puntos, deberíamos hacer funcionar:

Ingresar → cambia a Marketplace.
El nombre ingresado aparece en Marketplace.
Marketplace → Perfil.
Perfil → Marketplace.
Botones principales.
MDTextField.
ScreenManager.
get_screen().

Esto importa porque la rúbrica evalúa específicamente que la app ejecute y permita recorrer las pantallas, y que haya interacción mediante botones e inputs.

Es decir: no necesitamos hacer el Marketplace real; necesitamos hacer una maqueta funcional.

📁 Estructura que te recomiendo

Para este proyecto:

Marketplace_UCT/
│
├── main.py
├── marketplace.kv
├── README.md
├── FUNDAMENTACION-UX-UI.md
├── uso_ia.md
│
└── assets/
    └── ...

Esto además coincide con el criterio de organización del proyecto de la rúbrica, que pide una estructura ordenada y reproducible.

Y hay una cosa que necesito de ustedes antes de definir el diseño definitivo

La rúbrica le da 30 de los 100 puntos a la fundamentación UX/UI, y exige que las decisiones de diseño estén relacionadas con los resultados de sus entrevistas y encuestas.

Por eso no quiero inventar cosas como:

"Los estudiantes prefieren una pantalla sencilla"

si ustedes no obtuvieron ese resultado.

Si tienes el documento de las entrevistas/encuestas, resultados de la investigación o la encuesta que hicimos anteriormente, pásamelo y podemos diseñar el Marketplace basándonos en esos resultados. Así no solamente hacemos una app que se vea bonita: podemos justificar por qué cada pantalla, botón, texto y flujo está ahí, que es justamente lo que pide A3 de la rúbrica.

Después de eso podemos 
construir el main.py y marketplace.kv completos, paso a paso, y probarlos en tu Kivy antes de subirlos a GitHub.
