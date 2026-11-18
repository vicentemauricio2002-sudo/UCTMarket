import json
import time
from pathlib import Path

FILE = Path(__file__).resolve().parent / "analytics.json"


def registrar(nombre, datos=None):
    # Cargar el historial de eventos
    historial = []

    if FILE.exists():
        try:
            with open(FILE, "r", encoding="utf-8") as archivo:
                historial = json.load(archivo)

            if not isinstance(historial, list):
                print("[Analytics] Error: el JSON no contiene una lista.")
                return False

        except json.JSONDecodeError:
            print("[Analytics] Error: analytics.json está dañado.")
            return False

        except OSError as error:
            print(f"[Analytics] Error al leer: {error}")
            return False

    # Crear el nuevo evento
    evento = {
        "evento": nombre,
        "ts": time.time(),
        "datos": datos or {}
    }

    historial.append(evento)

    # Guardar el historial actualizado
    try:
        with open(FILE, "w", encoding="utf-8") as archivo:
            json.dump(
                historial,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        print(f"[Analytics] Registrado: {evento}")
        return True

    except OSError as error:
        print(f"[Analytics] Error al guardar: {error}")
        return False
