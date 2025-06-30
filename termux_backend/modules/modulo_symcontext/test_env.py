# test_env.py
import sys
import sqlite3
from pathlib import Path

# Añadir el directorio de módulos al sys.path
ROOT_DIR = Path(__file__).resolve().parents[2]  # ~/H-Brain/termux_backend
MODULES_DIR = ROOT_DIR / "modules"
sys.path.append(str(MODULES_DIR))

# Importar funciones utilitarias del mini SDK
try:
    from modulo_tools import get_settings, get_db_path
except ImportError as e:
    print("❌ Error importando modulo_tools:", e)
    sys.exit(1)

print("🚀 Iniciando test del entorno H-Brain...\n")

# --- Settings
try:
    settings = get_settings()
    print("✅ settings.json cargado:")
    for k, v in settings.items():
        print(f"  - {k}: {v}")
except Exception as e:
    print("❌ Error cargando settings.json:", e)
    sys.exit(1)

# --- Ruta a la base de datos
try:
    db_path = get_db_path()
    print(f"\n📁 Ruta base de datos: {db_path}")
    if not Path(db_path).exists():
        print("⚠️ Advertencia: La base de datos aún no existe.")
    else:
        print("✅ La base de datos existe.")
except Exception as e:
    print("❌ Error obteniendo la ruta de la base de datos:", e)
    sys.exit(1)

# --- Conexión SQLite + conteo de entradas
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM context_entries")
    total = cursor.fetchone()[0]
    print(f"\n📊 Entradas encontradas en 'context_entries': {total}")

    if total > 0:
        cursor.execute("SELECT id, input_text, purpose FROM context_entries ORDER BY id DESC LIMIT 3")
        rows = cursor.fetchall()
        print("📌 Últimas entradas:")
        for row in rows:
            print(f"  ID: {row[0]} | Propósito: {row[2]} | Texto: {row[1][:40]}...")

    conn.close()
except sqlite3.OperationalError as oe:
    print("❌ Error SQLite (quizá falta tabla 'context_entries'):", oe)
except Exception as e:
    print("❌ Error inesperado con SQLite:", e)
