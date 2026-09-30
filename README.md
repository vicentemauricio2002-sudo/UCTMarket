# Marketplace UCT

Aplicación de escritorio creada con Python 3.11, Kivy y KivyMD para mostrar un marketplace universitario. Permite ingresar un nombre, ver publicaciones de ejemplo y abrir el perfil.

## Requisitos previos

- Git
- Python 3.11
- PowerShell en Windows

## Cómo ejecutar el proyecto

Clona el repositorio y entra en la carpeta:

```powershell
git clone https://github.com/vicentemauricio2002-sudo/UCTMarket.git
cd UCTMarket
```

Crea un entorno virtual:

```powershell
python -m venv venv
```

Activa el entorno virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación habilita scripts solo para la sesión actual con el siguiente comando, y vuelve a intentar el comando anterior:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Instala las dependencias:

```powershell
python -m pip install --upgrade pip
```

```powershell
python -m pip install -r requirements.txt
```

Ejecuta la aplicación desde la carpeta del proyecto:

```powershell
python main.py
```

## Dependencias

Las dependencias están listadas en `requirements.txt`. Si modificas el entorno y quieres actualizar ese archivo, activa primero el entorno virtual y ejecuta:

```powershell
python -m pip freeze | Out-File -Encoding ascii requirements.txt
```

La opción `-Encoding ascii` evita que PowerShell escriba el archivo en UTF-16, formato que puede causar problemas al instalar las dependencias.

## Funcionalidades actuales

- Ingreso usando un nombre.
- Pantalla principal con publicaciones de ejemplo.
- Vista de perfil con el nombre ingresado.

El inicio de sesión no valida cuentas ni contraseñas. Las publicaciones son datos de ejemplo; la aplicación todavía no usa un servidor ni una base de datos.

## Estructura del proyecto

```text
UCTMarket/
├── main.py
├── marketplace.kv
├── requirements.txt
├── README.md
├── FUNDAMENTACION-UX- UI.md
├── .gitignore
└── uso_ia.md
```

`main.py` contiene la lógica de la aplicación y `marketplace.kv` define la interfaz. Mantén ambos archivos en la misma carpeta y conserva el nombre `marketplace.kv`.

## Nota sobre Git

El entorno virtual `venv/` es local y no debería subirse al repositorio. Comprueba que esté excluido mediante `.gitignore`.
