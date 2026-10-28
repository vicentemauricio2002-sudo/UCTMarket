"""Remote Config con valores predeterminados y tolerancia a fallos de red.

Configura UCTMARKET_REMOTE_CONFIG_URL como variable de entorno para usar un
endpoint JSON. Ejemplo de respuesta: {"welcome_message": "Bienvenido"}.
"""
import os
import requests

DEFAULT_CONFIG = {"welcome_message": "Bienvenido a UCTMarket", "primary_color": "#3B82F6"}
TIMEOUT_SECONDS = 3

def get_remote_config():
    url = os.environ.get("UCTMARKET_REMOTE_CONFIG_URL", "").strip()
    if not url:
        return DEFAULT_CONFIG.copy()
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            return DEFAULT_CONFIG.copy()
        config = DEFAULT_CONFIG.copy()
        if isinstance(data.get("welcome_message"), str) and data["welcome_message"].strip():
            config["welcome_message"] = data["welcome_message"].strip()
        if isinstance(data.get("primary_color"), str) and len(data["primary_color"]) == 7 and data["primary_color"].startswith("#"):
            config["primary_color"] = data["primary_color"]
        return config
    except (requests.RequestException, ValueError, TypeError) as exc:
        print(f"Remote Config: se usan valores predeterminados ({exc})")
        return DEFAULT_CONFIG.copy()

def get_welcome_message():
    return get_remote_config().get("welcome_message", DEFAULT_CONFIG["welcome_message"])
