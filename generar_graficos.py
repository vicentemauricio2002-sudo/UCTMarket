import matplotlib.pyplot as plt
from pathlib import Path
import json

# Carpeta donde se guardarán los gráficos
BASE_DIR = Path(__file__).resolve().parent
CARPETA_GRAFICOS = BASE_DIR / "graficos"
CARPETA_GRAFICOS.mkdir(exist_ok=True)

# Resultados obtenidos en analizador.py
nombres = [
    "Búsquedas con resultados",
    "Publicaciones exitosas",
    "Registro exitoso",
    "Interés en productos",
    "Interacción con lista de deseos"
]

valores = [80, 70, 70, 25, 20]

# Crear gráfico
plt.figure(figsize=(10, 6))

barras = plt.barh(nombres, valores)

# Mostrar porcentajes al final de cada barra
for barra, valor in zip(barras, valores):
    plt.text(
        valor + 1,
        barra.get_y() + barra.get_height() / 2,
        f"{valor}%",
        va="center"
    )

plt.title("Resultados de los KPI de UCTMarket")
plt.xlabel("Porcentaje (%)")
plt.xlim(0, 100)
plt.gca().invert_yaxis()

plt.tight_layout()

# Guardar imagen
ruta = CARPETA_GRAFICOS / "01_resumen_kpi.png"
plt.savefig(ruta, dpi=300, bbox_inches="tight")

plt.show()

print("Gráfico 01 guardado correctamente.")


# Segundo gráfico: interacciones con productos

eventos = [
    "Productos vistos",
    "Clics en comprar",
    "Agregados a deseos",
    "Eliminados de deseos"
]

cantidades = [20, 5, 4, 2]

plt.figure(figsize=(9, 5))

barras = plt.barh(eventos, cantidades)

for barra, cantidad in zip(barras, cantidades):
    plt.text(
        cantidad + 0.2,
        barra.get_y() + barra.get_height() / 2,
        str(cantidad),
        va="center"
    )

plt.title("Interacciones con productos en UCTMarket")
plt.xlabel("Cantidad de eventos")
plt.xlim(0, 23)
plt.gca().invert_yaxis()

plt.tight_layout()

ruta = CARPETA_GRAFICOS / "02_interacciones_productos.png"
plt.savefig(ruta, dpi=300, bbox_inches="tight")

plt.show()

print("Gráfico 02 guardado correctamente.")




# Tercer gráfico: resultados de los procesos principales

ARCHIVO_ANALYTICS = BASE_DIR / "analytics.json"

with open(ARCHIVO_ANALYTICS, "r", encoding="utf-8") as archivo:
    historial = json.load(archivo)

# Contadores iniciales
registro_exitoso = 0
registro_error = 0
publicacion_creada = 0
publicacion_error = 0

# Recorrer los eventos del historial
for evento in historial:
    nombre = evento.get("evento")

    if nombre == "registro_exitoso":
        registro_exitoso += 1
    elif nombre == "registro_error":
        registro_error += 1
    elif nombre == "publicacion_creada":
        publicacion_creada += 1
    elif nombre == "publicacion_error":
        publicacion_error += 1

# Datos para el gráfico
procesos = ["Registro", "Publicaciones"]
exitos = [registro_exitoso, publicacion_creada]
errores = [registro_error, publicacion_error]

posiciones = [0, 1]
ancho = 0.35

plt.figure(figsize=(9, 5))

barras_exitos = plt.barh(
    [p - ancho / 2 for p in posiciones],
    exitos,
    height=ancho,
    label="Exitosos"
)

barras_errores = plt.barh(
    [p + ancho / 2 for p in posiciones],
    errores,
    height=ancho,
    label="Errores"
)

# Mostrar cantidades sobre las barras
for barras in [barras_exitos, barras_errores]:
    for barra in barras:
        cantidad = barra.get_width()
        plt.text(
            cantidad + 0.1,
            barra.get_y() + barra.get_height() / 2,
            str(int(cantidad)),
            va="center"
        )

plt.yticks(posiciones, procesos)
plt.title("Resultados de los procesos principales")
plt.xlabel("Cantidad de eventos")
plt.xlim(0, max(exitos + errores) + 2)
plt.gca().invert_yaxis()
plt.legend()

plt.tight_layout()

ruta = CARPETA_GRAFICOS / "03_resultados_procesos.png"
plt.savefig(ruta, dpi=300, bbox_inches="tight")

plt.show()

print("Gráfico 03 guardado correctamente.")
