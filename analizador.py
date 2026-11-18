
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_ANALYTICS = BASE_DIR / "analytics.json"
ARCHIVO_PRODUCTOS = BASE_DIR / "productos.json"


def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def calcular_kpi():
    if not ARCHIVO_ANALYTICS.exists():
        print("Error: No se encontró analytics.json. Ejecuta primero generar_analytics.py.")
        return

    eventos = cargar_json(ARCHIVO_ANALYTICS)

    # Validar contra productos.json si existe en la carpeta
    ids_validos = None

    if ARCHIVO_PRODUCTOS.exists():
        productos = cargar_json(ARCHIVO_PRODUCTOS)

        if isinstance(productos, dict):
            lista_productos = productos.get("productos", [])
        elif isinstance(productos, list):
            lista_productos = productos
        else:
            lista_productos = []

        ids_validos = {
            p.get("id")
            for p in lista_productos
            if isinstance(p, dict) and p.get("id")
        }

    # Contadores de eventos
    busquedas_total = 0
    busquedas_con_coincidencias = 0
    publicaciones_creadas = 0
    publicaciones_error = 0
    registros_exitosos = 0
    registros_error = 0
    productos_vistos = 0
    clics_comprar = 0
    deseos_agregados = 0
    deseos_eliminados = 0

    for ev in eventos:
        nombre = ev.get("evento")
        datos = ev.get("datos", {})

        # Validación opcional de integridad de IDs
        if ids_validos is not None and nombre in {
            "producto_visto",
            "click_comprar",
            "lista_deseos_agregada",
            "lista_deseos_eliminada",
        }:
            pid = datos.get("producto_id")
            if pid not in ids_validos:
                print(f"Advertencia: ID no encontrado en productos.json -> {pid}")

        if nombre == "busqueda_realizada":
            busquedas_total += 1
            if datos.get("con_coincidencias") is True:
                busquedas_con_coincidencias += 1
        elif nombre == "publicacion_creada":
            publicaciones_creadas += 1
        elif nombre == "publicacion_error":
            publicaciones_error += 1
        elif nombre == "registro_exitoso":
            registros_exitosos += 1
        elif nombre == "registro_error":
            registros_error += 1
        elif nombre == "producto_visto":
            productos_vistos += 1
        elif nombre == "click_comprar":
            clics_comprar += 1
        elif nombre == "lista_deseos_agregada":
            deseos_agregados += 1
        elif nombre == "lista_deseos_eliminada":
            deseos_eliminados += 1

    # Cálculos con protección contra división por cero
    kpi_busquedas = (busquedas_con_coincidencias / busquedas_total * 100) if busquedas_total else 0
    total_pub = publicaciones_creadas + publicaciones_error
    kpi_publicaciones = (publicaciones_creadas / total_pub * 100) if total_pub else 0
    kpi_interes = (clics_comprar / productos_vistos * 100) if productos_vistos else 0
    total_reg = registros_exitosos + registros_error
    kpi_registro = (registros_exitosos / total_reg * 100) if total_reg else 0
    kpi_deseos = (deseos_agregados / productos_vistos * 100) if productos_vistos else 0

    print("=" * 55)
    print("REPORTE DE KPI — UCTMarket (Datos Sintéticos)")
    print("=" * 55)
    print(f"Total de eventos procesados: {len(eventos)}\n")
    print(f"1. Tasa de búsquedas con resultados : {kpi_busquedas:.1f}% ({busquedas_con_coincidencias}/{busquedas_total})")
    print(f"2. Tasa de publicaciones exitosas   : {kpi_publicaciones:.1f}% ({publicaciones_creadas}/{total_pub})")
    print(f"3. Tasa de interés en productos     : {kpi_interes:.1f}% ({clics_comprar}/{productos_vistos})")
    print(f"4. Tasa de éxito del registro       : {kpi_registro:.1f}% ({registros_exitosos}/{total_reg})")
    print(f"5. Interacción con lista de deseos  : {kpi_deseos:.1f}% ({deseos_agregados}/{productos_vistos})")
    print(f"   (Eliminaciones de lista deseos   : {deseos_eliminados} eventos registrados)")
    print("=" * 55)


if __name__ == "__main__":
    calcular_kpi()
