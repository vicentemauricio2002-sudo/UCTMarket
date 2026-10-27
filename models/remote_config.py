import urllib.request
import json

DEFAULT_WELCOME_MESSAGE = 'Bienvenido a UCTMarket'

def get_remote_value():
    """
    Intenta obtener el mensaje de bienvenida desde el servidor Flask remoto.
    Si el servidor no está encendido o falla la red, la función falla
    y 'get_welcome_message' usará el DEFAULT_WELCOME_MESSAGE de respaldo.
    """
    url = "http://127.0.0.1:5000/config_remota"
    
    # Hacemos una petición HTTP simple con la librería estándar de Python
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=2) as response:
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('mensaje_bienvenida')
            
    return None

def get_welcome_message():
    try:
        value = get_remote_value()
        if value:
            return str(value)
    except Exception:
        # Si el servidor remoto falla o no responde, entra aquí
        pass
    return DEFAULT_WELCOME_MESSAGE