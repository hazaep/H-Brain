import sys
from pathlib import Path

# Agrega la raíz del proyecto al sys.path
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR / "termux_backend" / "modules"))

from modulo_tools import get_settings, get_db_path

print("Settings:", get_settings())
print("DB path: ", get_db_path())
