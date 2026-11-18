import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Fecha de inicio de la simulación.
# Se utiliza el horario de Chile continental (UTC-3).
inicio = datetime(
    2026, 11, 17, 10, 0, 0,
    tzinfo=timezone(timedelta(hours=-3))
)

# IDs de los 20 productos actuales.
productos = [
    "baad622c-796f-4a2c-8bbb-4b8916b64829",
    "dc7ac20f-a840-44be-b213-80fcdb995304",
    "0f050640-e78f-441d-bc82-701466465f75",
    "f696526b-e7c9-48a7-a8af-2fc7fff8f8d5",
    "8972c617-6f16-4d3f-9fac-b3969fe0537b",
    "dee8fc55-ef6a-4d8b-807f-5b18123c9d8c",
    "05d35351-ec0f-47cd-8493-a19b56768a90",
    "14f25b99-9408-45eb-9afa-2edbe1cdc197",
    "36f4036d-e27f-487c-8c15-090f4d22c4fb",
    "a3a8b265-d102-4321-b291-0fb240710e49",
    "72eb595e-88fe-45a3-86e1-e0fde6180e46",
    "6c8d3797-2f0a-4639-b304-b53a9afd7ea6",
    "9943779e-d5d5-49aa-ae29-7d0e216f7a1f",
    "137cafc8-ccd8-4256-b689-cbfaf77b7c70",
    "6ca3864d-2aaa-4fa4-8c17-ed23a070cbcd",
    "95a2c3ca-e89b-4437-9489-6e90b882e54d",
    "ba125cca-07a2-40bd-b1f6-53c92daa0f85",
    "6cfdc8a0-f9d3-44f8-970e-d11d0e423c5f",
    "e93924b6-f59f-464a-820a-726d5079f84c",
    "90994500-94bd-42c9-9b67-1eee1a347b45"
]

eventos = []


def registrar(nombre, datos=None, segundos=0):
    fecha = inicio + timedelta(seconds=segundos)

    eventos.append({
        "evento": nombre,
        "ts": fecha.timestamp(),
        "datos": datos or {}
    })


# Navegación.
registrar("pantalla_vista", {"nombre": "login"}, 0)
registrar("pantalla_vista", {"nombre": "registro"}, 15)

# KPI 4: registro.
registros = [
    ("registro_exitoso", {}),
    ("registro_error", {"motivo": "nombre_vacio"}),
    ("registro_exitoso", {}),
    ("registro_error", {"motivo": "contrasena_vacia"}),
    ("registro_exitoso", {}),
    ("registro_exitoso", {}),
    ("registro_error", {
        "motivo": "nombre_existente_o_datos_invalidos"
    }),
    ("registro_exitoso", {}),
    ("registro_exitoso", {}),
    ("registro_exitoso", {})
]

for i, (nombre, datos) in enumerate(registros):
    registrar(nombre, datos, 60 + i * 23)

registrar("pantalla_vista", {"nombre": "login"}, 310)


# KPI 2: publicaciones.
# Los UUID representan publicaciones sintéticas históricas.

for i in range(5):
    producto_id = str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"uctmarket-sim-publicacion-{i + 1}"
        )
    )

    registrar(
        "publicacion_creada",
        {"producto_id": producto_id},
        360 + i * 29
    )

errores_publicacion = [
    "campos_incompletos_nombre_precio_descripcion",
    "precio_invalido",
    "whatsapp_invalido",
    "error_al_guardar_imagen",
    "error_al_guardar_publicacion"
]

for i, motivo in enumerate(errores_publicacion):
    registrar(
        "publicacion_error",
        {"motivo": motivo},
        580 + i * 31
    )


# KPI 1: búsquedas.
registrar("pantalla_vista", {"nombre": "market"}, 700)

for i, coincidencias in enumerate(
    [True, True, True, True, False]
):
    registrar(
        "busqueda_realizada",
        {"con_coincidencias": coincidencias},
        730 + i * 35
    )

# KPI 3 y KPI 5: vistas de productos.
tiempos_vistas = []

for i, producto_id in enumerate(productos):
    segundo = 950 + i * 24
    tiempos_vistas.append(segundo)

    registrar(
        "producto_visto",
        {"producto_id": producto_id},
        segundo
    )

# Cinco clics de contacto.
for indice in [1, 4, 7, 12, 18]:
    registrar(
        "click_comprar",
        {"producto_id": productos[indice]},
        tiempos_vistas[indice] + 8
    )

# Cuatro adiciones a la lista de deseos.
for indice in [0, 3, 6, 10]:
    registrar(
        "lista_deseos_agregada",
        {"producto_id": productos[indice]},
        tiempos_vistas[indice] + 11
    )

# Dos eliminaciones de la lista de deseos.
for indice in [3, 10]:
    registrar(
        "lista_deseos_eliminada",
        {"producto_id": productos[indice]},
        tiempos_vistas[indice] + 16
    )

# Orden cronológico.
eventos.sort(key=lambda evento: evento["ts"])

# Validaciones de cantidades.
def contar(nombre):
    return sum(
        1 for evento in eventos
        if evento["evento"] == nombre
    )


assert contar("busqueda_realizada") == 5
assert contar("publicacion_creada") == 5
assert contar("publicacion_error") == 5
assert contar("registro_exitoso") == 7
assert contar("registro_error") == 3
assert contar("producto_visto") == 20
assert contar("click_comprar") == 5
assert contar("lista_deseos_agregada") == 4
assert contar("lista_deseos_eliminada") == 2

# Verificar que los IDs de interacción sean válidos.
for evento in eventos:
    if evento["evento"] in [
        "producto_visto",
        "click_comprar",
        "lista_deseos_agregada",
        "lista_deseos_eliminada"
    ]:
        assert evento["datos"]["producto_id"] in productos

# Guardar el nuevo historial.
archivo = Path(__file__).resolve().parent / "analytics.json"

with open(archivo, "w", encoding="utf-8") as f:
    json.dump(
        eventos,
        f,
        ensure_ascii=False,
        indent=4
    )

print("Analytics generado correctamente.")
print(f"Archivo: {archivo}")
print(f"Total de eventos: {len(eventos)}")

print("\nResumen:")
for nombre in sorted(set(e["evento"] for e in eventos)):
    print(f"{nombre}: {contar(nombre)}")