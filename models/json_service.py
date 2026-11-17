import json
import uuid
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / 'data' / 'usuarios.json'

def load_data():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists(): DATA_FILE.write_text('{"usuarios": []}', encoding='utf-8')
    try: return json.loads(DATA_FILE.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError): return {'usuarios': []}

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding='utf-8')

def get_user(nombre, contrasena):
    data = load_data()
    nombre = nombre.strip()

    for u in data['usuarios']:
        if (
            u.get('nombre', '').lower() == nombre.lower()
            and u.get('contrasena', '') == contrasena
        ):
            return u

    return None

def create_user(nombre, contrasena):
    data = load_data()
    nombre = nombre.strip()

    if not nombre or not contrasena:
        return None

    for u in data['usuarios']:
        if u.get('nombre', '').lower() == nombre.lower():
            return None

    usuario = {
        'nombre': nombre,
        'contrasena': contrasena,
        'usuarioFoto': "imgs/img_perfiles/placeholder.png",
        'historial': [],
        'listaDeseos': []
    }

    data['usuarios'].append(usuario)
    save_data(data)

    return usuario

def save_user(usuario):
    try:
        data = load_data()

        for i, u in enumerate(data['usuarios']):
            if u.get('nombre', '').lower() == usuario.get('nombre', '').lower():
                data['usuarios'][i] = usuario
                save_data(data)
                return True

        data['usuarios'].append(usuario)
        save_data(data)
        return True

    except (OSError, TypeError, ValueError) as error:
        print("Error al guardar el usuario:", error)
        return False

def cargar_productos():
    ruta = DATA_FILE.parent / "productos.json"

    if not ruta.exists():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(
            '{"productos": []}',
            encoding="utf-8"
        )

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        productos = datos.get("productos", [])

        if not isinstance(productos, list):
            return []

        # Asignar identificadores a publicaciones antiguas.
        modificados = False

        for producto in productos:
            if not producto.get("id"):
                producto["id"] = str(uuid.uuid4())
                modificados = True

        # Guardar los identificadores nuevos en el JSON.
        if modificados:
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=4
                )

        return productos

    except (json.JSONDecodeError, OSError, TypeError, AttributeError) as error:
        print("Error al cargar los productos:", error)
        return []

def guardar_producto(producto):
    ruta = DATA_FILE.parent / "productos.json"

    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)

        if ruta.exists():
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        else:
            datos = {"productos": []}

        if not isinstance(datos.get("productos"), list):
            datos["productos"] = []

        datos["productos"].append(producto)

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        return True

    except (json.JSONDecodeError, OSError, TypeError) as error:
        print("Error al guardar el producto:", error)
        return False

def actualizar_producto(producto_id, producto):
    ruta = DATA_FILE.parent / "productos.json"

    try:
        if not ruta.exists():
            return False

        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        productos = datos.get("productos", [])

        for indice, producto_guardado in enumerate(productos):
            if producto_guardado.get("id") == producto_id:

                productos[indice] = producto

                with open(ruta, "w", encoding="utf-8") as archivo:
                    json.dump(
                        datos,
                        archivo,
                        ensure_ascii=False,
                        indent=4
                    )

                return True

        print("No se encontró la publicación para actualizar.")
        return False

    except (json.JSONDecodeError, OSError, TypeError) as error:
        print("Error al actualizar el producto:", error)
        return False

def eliminar_producto(producto_id):
    ruta = DATA_FILE.parent / "productos.json"

    try:
        if not ruta.exists():
            return False

        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        productos = datos.get("productos", [])

        for indice, producto_guardado in enumerate(productos):
            if producto_guardado.get("id") == producto_id:

                productos.pop(indice)

                with open(ruta, "w", encoding="utf-8") as archivo:
                    json.dump(
                        datos,
                        archivo,
                        ensure_ascii=False,
                        indent=4
                    )

                return True

        print("No se encontró la publicación para eliminar.")
        return False

    except (json.JSONDecodeError, OSError, TypeError) as error:
        print("Error al eliminar el producto:", error)
        return False