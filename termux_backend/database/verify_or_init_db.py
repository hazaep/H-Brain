import sqlite3
from pathlib import Path
from termux_backend.modules.modulo_tools.utils import get_db_path

def tabla_existe(nombre_tabla, cursor):
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
    """, (nombre_tabla,))
    return cursor.fetchone() is not None

def cargar_schema_si_falta():
    db_path = Path(get_db_path())
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if not tabla_existe("context_entries", cursor):
        print("⚠️ Tabla 'context_entries' no encontrada. Cargando esquema desde schema.sql...")

        # Ruta al schema.sql (está al lado de context.db)
        schema_path = db_path.parent / "schema.sql"
        if not schema_path.exists():
            print(f"❌ No se encontró el archivo: {schema_path}")
            conn.close()
            return

        with open(schema_path, "r") as f:
            sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()
            print("✅ Esquema de base de datos inicializado correctamente.")
    else:
        print("✅ Tabla 'context_entries' ya existe. Todo en orden.")

    conn.close()

if __name__ == "__main__":
    cargar_schema_si_falta()
