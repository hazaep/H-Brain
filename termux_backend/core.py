# core.py

import os
import importlib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # ~/H-Brain/
MODULES_PATH = Path(__file__).parent / "modules"
CONFIG_PATH = BASE_DIR / "configs" / "settings.json"

class AutomationCore:
    def __init__(self, config_path=CONFIG_PATH):
        self.config = self.load_config(config_path)
        self.modules = self.load_modules()

    def load_config(self, path):
        try:
            with open(path, "r") as f:
                print(f"🧠 Config loaded from: {path}")
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config file not found: {path}")
            return {}
        except json.JSONDecodeError:
            print(f"❌ Error parsing JSON config: {path}")
            return {}

    def load_modules(self):
        modules = {}
        enabled_modules = self.config.get("modules_enabled", [])
        for module_name in enabled_modules:
            try:
                mod = importlib.import_module(f"modules.{module_name}")
                modules[module_name] = mod
                print(f"✅ Module loaded: {module_name}")
            except Exception as e:
                print(f"❌ Error loading module '{module_name}': {e}")
        return modules

    def execute_command(self, module_name, command_name, **kwargs):
        if module_name not in self.modules:
            return {"error": f"Module '{module_name}' not found."}

        module = self.modules[module_name]
        if hasattr(module, command_name):
            func = getattr(module, command_name)
            try:
                return func(**kwargs)
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"error": f"Command '{command_name}' not found in module '{module_name}'."}
