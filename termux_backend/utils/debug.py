# termux_backend/utils/debug.py
import os, json

_cfg_path = os.path.expanduser("~/H-Brain/configs/settings.json")
with open(_cfg_path) as f:
    _cfg = json.load(f)

DEBUG = _cfg.get("debug", False)

def log_debug(message):
    if DEBUG:
        print(f"[DEBUG] {message}")
