import json
import os

def get_neurobank_db_path():
    settings_path = os.path.expanduser("~/H-Brain/configs/settings.json")
    with open(settings_path, "r") as f:
        settings = json.load(f)
    return os.path.expanduser(os.path.join(
        "~/H-Brain", settings.get("neurobank_db_path", "termux_backend/database/naurobank_vault.db")
    ))
