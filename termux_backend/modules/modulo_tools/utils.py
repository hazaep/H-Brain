# modulo_tools/utils.py
import os
import json
from pathlib import Path

_cfg_path = os.path.expanduser("~/H-Brain/configs/settings.json")
with open(_cfg_path) as f:
    _cfg = json.load(f)

DEBUG = _cfg.get("debug", False)

def log_debug(message):
    if DEBUG:
        print(f"[DEBUG] {message}")

def get_settings():
    base = Path(__file__).resolve().parents[3]
    cfg = base / "configs" / "settings.json"
    try:
        with open(cfg, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ No se pudo cargar settings.json: {e}")
        return {}

def get_db_path():
    settings = get_settings()
    db_rel = settings.get("context_db_path", "termux_backend/database/context.db")
    base = Path(__file__).resolve().parents[3]
    return str((base / db_rel).resolve())

def get_secret(key_name):
    settings = get_settings()
    rel = settings.get(f"{key_name}_key_path")
    if not rel:
        print(f"⚠️ No hay ruta para {key_name}_key_path en settings.json")
        return None
    base = Path(__file__).resolve().parents[3]
    secret_file = base / rel
    try:
        return secret_file.read_text().strip()
    except Exception as e:
        print(f"❌ Error al leer la clave '{key_name}': {e}")
        return None

def get_log_path(nombre_archivo="user_inputs.log"):
    base_path = Path(__file__).resolve().parents[3]
    log_dir = base_path / "termux_backend/database/logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return str((log_dir / nombre_archivo).resolve())
