# UCTMarket

Marketplace académico desarrollado como proyecto práctico de Desarrollo Móvil para la comunidad universitaria de la Universidad Católica de Temuco (UCT).

La aplicación permite a estudiantes y docentes publicar productos, explorar publicaciones, buscar artículos de interés, guardar productos en una lista de deseos y contactar directamente con los vendedores mediante WhatsApp.

El proyecto está desarrollado con **Python y KivyMD 2.0.0**, utiliza archivos JSON para la persistencia local y Flask para proporcionar configuración remota.

## Arquitectura y patrón MVC

El proyecto organiza sus responsabilidades siguiendo una estructura basada en el patrón **Modelo-Vista-Controlador (MVC)**:

- **Modelo (`models/`):** gestiona la persistencia de datos mediante JSON (`json_service.py`), las notificaciones locales (`notification_service.py`) y la comunicación con el servidor de configuración remota (`remote_config.py`).
- **Vista (`views/`):** contiene la interfaz gráfica desarrollada con KivyMD, definida en `marketplace.kv`.
- **Controlador (`controllers/`):** administra la navegación, las funcionalidades y los eventos de la aplicación mediante `main.py`. También contiene `app.py`, encargado del servidor backend desarrollado con Flask.

## Funcionalidades principales

- Registro e inicio de sesión de usuarios.
- Exploración y búsqueda de publicaciones.
- Creación, edición y eliminación de publicaciones.
- Visualización de información de productos.
- Lista de deseos para guardar y administrar productos de interés.
- Contacto directo con vendedores mediante WhatsApp y mensajes predefinidos.
- Persistencia local de usuarios y productos mediante archivos JSON.
- Registro de eventos de interacción para analizar el uso de la aplicación.
- Configuración remota mediante un servidor Flask, con mecanismo de respaldo ante fallos de conexión.

## Requisitos previos

- Python 3.10 o superior.
- Git instalado en el equipo.
- KivyMD 2.0.0 (se instala mediante las dependencias del proyecto).

---

## Guía de instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/vicentemauricio2002-sudo/UCTMarket.git
cd UCTMarket
```

### 2. Crear y activar el entorno virtual

En Windows (PowerShell):

Crear el entorno virtual:

```bash
python -m venv venv
```

Activarlo:

```powershell
.\venv\Scripts\Activate.ps1
```

**Si aparece un error de seguridad al activar el entorno virtual:**

PowerShell puede bloquear la ejecución de scripts por su política de seguridad. Para permitir la activación temporalmente en la terminal actual, ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Si solicita confirmación, aceptar y volver a ejecutar:

```powershell
.\venv\Scripts\Activate.ps1
```

Esta configuración solo se mantiene mientras la ventana de PowerShell permanezca abierta. Al cerrarla, se restaura la política anterior.

En Linux / macOS:

Crear el entorno virtual:

```bash
python3 -m venv venv
```

Activarlo:

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

Con el entorno virtual activado:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Ejecución de la aplicación

Para ejecutar el proyecto se recomienda utilizar dos terminales, ambas ubicadas en la carpeta raíz del repositorio y con el entorno virtual activado.

### Terminal 1: Servidor backend Flask

```bash
python controllers/app.py
```

El servidor se ejecutará localmente en:

`http://127.0.0.1:5000`

Este servicio proporciona la configuración remota utilizada por la aplicación.

### Terminal 2: Aplicación UCTMarket

```bash
python controllers/main.py
```

La aplicación iniciará su interfaz gráfica y podrá utilizar las funcionalidades disponibles.

---

## Persistencia de datos

UCTMarket utiliza archivos JSON para almacenar información localmente:

- `data/productos.json`: contiene las publicaciones de productos.
- `data/usuarios.json`: almacena la información de los usuarios y sus datos asociados, como la lista de deseos.
- `analytics.json`: almacena el historial de eventos registrados durante el uso de la aplicación.

La persistencia permite conservar la información entre ejecuciones de la aplicación.

## Sistema de analítica y evaluación

El proyecto incorpora un sistema de analítica desarrollado en Python para registrar y estudiar las interacciones realizadas dentro de la aplicación.

- `analytics.py`: registra eventos con su nombre, marca de tiempo y datos asociados.
- `analytics.json`: almacena el historial de eventos en formato JSON.
- `analizador.py`: procesa los eventos registrados y calcula indicadores clave de rendimiento (KPI).
- `generar_graficos.py`: utiliza Matplotlib para generar representaciones gráficas de los resultados.
- `graficos/`: contiene los gráficos obtenidos durante el análisis.

Entre los indicadores evaluados se encuentran:

- Tasa de búsquedas con resultados.
- Tasa de publicaciones exitosas.
- Tasa de interés en productos.
- Tasa de éxito del registro.
- Interacción con la lista de deseos.

**Consideración sobre los resultados:** los datos utilizados para los gráficos corresponden a un escenario de pruebas sintético diseñado con apoyo de inteligencia artificial y autorizado para la evaluación académica. Por lo tanto, los resultados representan una simulación de interacciones y no mediciones realizadas con usuarios reales.

Los eventos de analítica no almacenan contraseñas, números de WhatsApp ni textos de búsqueda.

---

## Estructura del repositorio

```text
UCTMarket/
│
├── controllers/
│   ├── app.py                  # Controlador backend en Flask (API de config remota)
│   └── main.py                 # Controlador principal de Kivy (navegación y eventos)
│
├── data/
│   ├── productos.json          # Datos persistentes de productos guardados por JSON
│   └── usuarios.json           # Datos persistentes de usuarios guardados por JSON        
│
├── graficos/
│   ├── 01_resumen_kpi.png                  # Grafico creado con Matplotlib
│   ├── 02_interacciones_productos.png      # Grafico creado con Matplotlib 
│   └── 03_resultados_procesos.png          # Grafico creado con Matplotlib 
│
├── imgs/
│   ├── img_perfiles/           # Carpeta que guarda placeholder e imagenes de fotos de perfil
│   └── img_productos/          # Carpeta que guarda placeholder e imagenes de productos
│
├── models/
│   ├── json_service.py                     # Funciones para manejo de datos JSON
│   ├── notification_service.py             # Función para notificaciones con Plyer
│   └── remote_config.py                    # Configuración remota por servidor Flask
│
├── views/
│   └── marketplace.kv          # Interfaz gráfica y diseño visual de pantallas
│
├── .gitignore                  # Archivos y carpetas ignoradas al subir a repositorio
├── analizador.py               # Analiza los eventos registrados y calcula los KPI de UCTMarket.
├── analytics.json              # Historial de eventos y datos sintéticos utilizados para evaluar la aplicación.
├── analytics.py                # Módulo encargado de registrar eventos de uso y almacenarlos en analytics.json.
├── FUNDAMENTACION-UX-UI.md     # Documentación que fundamenta las decisiones de diseño UX/UI de la aplicación.
├── generar_graficos.py         # Procesa los datos de analytics.json y genera gráficos estadísticos mediante Matplotlib.
├── README.md                   # Documentación principal del proyecto, instalación, ejecución y características.
├── requirements.txt            # Lista de bibliotecas y dependencias necesarias para ejecutar el proyecto.
└── uso_ia.md                   # Declaración acerca del uso de la IA en este proyecto
```

## Guía de pruebas para la defensa

### 1. Prueba de autenticación

- Ejecutar la aplicación.
- Registrar un usuario de prueba.
- Iniciar sesión con sus credenciales.
- Comprobar el comportamiento ante credenciales incorrectas.

### 2. Prueba de publicaciones

- Crear una publicación con nombre, descripción, precio e imagen.
- Comprobar que aparece en el marketplace.
- Editar la publicación.
- Eliminarla y verificar que los cambios se reflejan en los datos persistentes.

### 3. Prueba de lista de deseos

- Abrir una publicación.
- Agregar el producto a la lista de deseos.
- Revisar que aparezca en la sección correspondiente.
- Eliminarlo de la lista y comprobar que se actualice.

### 4. Prueba de contacto mediante WhatsApp

- Abrir una publicación que tenga un número de contacto configurado.
- Presionar el botón de compra o contacto.
- Verificar que se abra WhatsApp con el mensaje de consulta predefinido.

### 5. Prueba de persistencia

- Realizar cambios en los datos de la aplicación.
- Cerrar y volver a ejecutar UCTMarket.
- Comprobar que los datos se mantienen después de reiniciar la aplicación.

### 6. Prueba de configuración remota

- Ejecutar el servidor Flask en la primera terminal.
- Iniciar la aplicación en la segunda terminal.
- Comprobar que se obtiene la configuración remota.
- Detener el servidor mediante `Ctrl + C`.
- Volver a iniciar o recargar la aplicación y comprobar que utiliza su configuración de respaldo sin interrumpir el funcionamiento.

---

## Tecnologías utilizadas

- **Python:** lenguaje principal del proyecto.
- **Kivy:** framework para el desarrollo de aplicaciones multiplataforma.
- **KivyMD 2.0.0:** componentes e interfaz gráfica.
- **Flask:** servidor backend para configuración remota.
- **JSON:** persistencia local de datos y almacenamiento de eventos.
- **Matplotlib:** generación de gráficos estadísticos.
- **Plyer:** integración de notificaciones locales.
- **UUID:** generación de identificadores únicos para las publicaciones.

## Uso de inteligencia artificial

Se utilizó inteligencia artificial como herramienta de apoyo durante el desarrollo, la resolución de problemas técnicos y la preparación del escenario sintético de evaluación.

Los detalles de su utilización se encuentran documentados en `uso_ia.md`.
