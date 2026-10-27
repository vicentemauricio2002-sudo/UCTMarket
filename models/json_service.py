import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent.parent / 'data' / 'usuarios.json'

def load_data():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists(): DATA_FILE.write_text('{"usuarios": []}', encoding='utf-8')
    try: return json.loads(DATA_FILE.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError): return {'usuarios': []}

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding='utf-8')

def get_or_create_user(nombre):
    data=load_data(); nombre=nombre.strip()
    for u in data['usuarios']:
        if u.get('nombre','').lower()==nombre.lower(): return u
    u={'nombre':nombre,'tareas':[]}; data['usuarios'].append(u); save_data(data); return u

def save_user(usuario):
    data=load_data()
    for i,u in enumerate(data['usuarios']):
        if u.get('nombre','').lower()==usuario.get('nombre','').lower():
            data['usuarios'][i]=usuario; save_data(data); return
    data['usuarios'].append(usuario); save_data(data)
