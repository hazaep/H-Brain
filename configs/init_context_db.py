import sqlite3
import os
import json

# Cargar configuración desde settings.json
CONFIG_PATH = os.path.expanduser("~/H-Brain/configs/settings.json")

with open(CONFIG_PATH, "r") as f:
    settings = json.load(f)

DB_PATH = os.path.expanduser(f"~/H-Brain/{settings['db_path']}")

# Crear carpeta si no existe
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Conectar a la base de datos
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS context_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    purpose TEXT,
    identity_mode TEXT,
    tension TEXT,
    tags TEXT
)
""")

# Verificar si la columna embedding existe
cursor.execute("PRAGMA table_info(context_entries)")
columnas = [col[1] for col in cursor.fetchall()]
if "embedding" not in columnas:
    cursor.execute("ALTER TABLE context_entries ADD COLUMN embedding TEXT")
    print("🧬 Columna 'embedding' agregada correctamente.")
else:
    print("✅ Columna 'embedding' ya existe.")

conn.commit()
conn.close()
print(f"📁 Base de datos inicializada en: {DB_PATH}")
