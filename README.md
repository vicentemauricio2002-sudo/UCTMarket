# UCTMarket - Evaluación N°3

Proyecto práctico de Desarrollo Móvil con Kivy y backend en Flask estructurado bajo el patrón **Modelo-Vista-Controlador (MVC)** para la comunidad universitaria UCT.

## Arquitectura y Patrón MVC
El proyecto separa sus responsabilidades en tres capas principales:
- **Modelo (`models/`):** Gestiona la lógica de datos, persistencia local en JSON (`json_service.py`), notificaciones de escritorio (`notification_service.py`) y la conexión HTTP remota con manejo de tolerancia a fallos (`remote_config.py`).
- **Vista (`views/`):** Contiene la interfaz gráfica de usuario desarrollada con componentes de KivyMD (`marketplace.kv`).
- **Controlador (`controllers/`):** Administra la lógica de navegación de la aplicación móvil (`main.py`) y el servidor backend local (`app.py`).

---

## Requisitos previos
- Python 3.10 o superior.
- Git instalado en el equipo.

---

## Guía de instalación y configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/UCTMarket.git
cd UCTMarket
```

### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\Activate
```

En Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## Instrucciones para la Demo en Vivo (2 Terminales)

Para demostrar la integración cliente-servidor, mantén dos terminales abiertas con el entorno virtual activado (`.\venv\Scripts\Activate`):

### Terminal 1: Servidor Backend (Controlador Remoto)
Ejecuta el servidor Flask desde la raíz del proyecto:
```bash
python controllers/app.py
```
> El servidor se ejecutará en `http://127.0.0.1:5000`.

### Terminal 2: Aplicación Móvil (Controlador Kivy)
En una **segunda terminal**, ejecuta la app principal desde la raíz del proyecto:
```bash
python controllers/main.py
```

---

## Estructura del repositorio
```text
UCTMarket-main/
│
├── Controlador/
│   ├── main.py                 # Controlador principal de Kivy (navegación y eventos)
│   └── app.py                  # Controlador backend en Flask (API de config remota)
│
├── Vista/
│   └── marketplace.kv          # Interfaz gráfica y diseño visual de pantallas
│
├── Modelo/
│   ├── json_service.py         # Lógica de persistencia local de usuarios y tareas
│   ├── notification_service.py # Servicio de alertas locales mediante plyer
│   └── remote_config.py        # Peticiones HTTP y sistema de respaldo (Fallback)
│
├── data/
│   └── usuarios.json           # Base de datos local persistente
│
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Documentación oficial
```

---

## Guía de pruebas para la defensa

1. **Prueba de Servicio Remoto:**
   - Con `python controllers/app.py` corriendo en la Terminal 1 y `python controllers/main.py` en la Terminal 2, inicia sesión en la app. El mensaje superior mostrará el texto obtenido desde el servidor: `"Bienvenido a UCTMarket Oficial (Desde Servidor)"`.

2. **Prueba de Persistencia y Notificación:**
   - Registra una tarea. Se disparará la notificación local y los datos se grabarán en `data/usuarios.json`. Cierra y reabre la app para validar que persisten.

3. **Prueba de Tolerancia a Fallos (Servidor Caído):**
   - Detén el servidor Flask en la Terminal 1 presionando `Ctrl + C`.
   - Vuelve a iniciar o recargar la app de Kivy. La aplicación detectará el fallo de red, activará el mecanismo de respaldo y cargará por defecto el mensaje `DEFAULT_WELCOME_MESSAGE` sin romperse.