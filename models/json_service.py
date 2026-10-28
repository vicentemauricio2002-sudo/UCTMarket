"""Persistencia local JSON para usuarios de UCTMarket."""
import json
import os
import secrets
import hashlib
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
USERS_FILE = DATA_DIR / "usuarios.json"

def _ensure_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        _write_users([])

def _read_users():
    _ensure_storage()
    try:
        with USERS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        # No se cierra la app si el JSON está dañado o no se puede leer.
        return []

def _write_users(users):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = USERS_FILE.with_suffix(".tmp")
    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=2)
    temp_file.replace(USERS_FILE)

def _password_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000).hex()

def register_user(nombre, password):
    nombre = nombre.strip()
    if not nombre or not password:
        return False, "Ingresa un nombre y una contraseña."
    users = _read_users()
    if any(u.get("nombre", "").casefold() == nombre.casefold() for u in users):
        return False, "Ese nombre de usuario ya está registrado."
    salt = secrets.token_hex(16)
    users.append({"nombre": nombre, "salt": salt, "password_hash": _password_hash(password, salt), "tareas": []})
    try:
        _write_users(users)
    except OSError:
        return False, "No se pudieron guardar los datos. Revisa los permisos de la carpeta."
    return True, "Cuenta creada. Ahora puedes iniciar sesión."

def authenticate_user(nombre, password):
    nombre = nombre.strip()
    if not nombre or not password:
        return None
    for user in _read_users():
        if user.get("nombre", "").casefold() == nombre.casefold():
            salt = user.get("salt", "")
            expected = user.get("password_hash", "")
            if salt and expected and secrets.compare_digest(_password_hash(password, salt), expected):
                return {"nombre": user.get("nombre", nombre), "tareas": user.get("tareas", [])}
            return None
    return None

def save_user(user):
    users = _read_users()
    nombre = user.get("nombre", "")
    for index, stored in enumerate(users):
        if stored.get("nombre", "").casefold() == nombre.casefold():
            stored["tareas"] = user.get("tareas", [])
            users[index] = stored
            try:
                _write_users(users)
                return True
            except OSError:
                return False
    return False

def get_or_create_user(nombre):
    """Compatibilidad con versiones anteriores; no crea cuentas sin contraseña."""
    for user in _read_users():
        if user.get("nombre", "").casefold() == nombre.strip().casefold():
            return {"nombre": user.get("nombre", nombre), "tareas": user.get("tareas", [])}
    return {"nombre": nombre.strip(), "tareas": []}
