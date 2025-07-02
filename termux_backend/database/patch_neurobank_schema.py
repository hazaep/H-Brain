import sqlite3
from termux_backend.modules.modulo_tools.utils import get_db_path

DB_PATH = get_db_path()

def add_column_if_not_exists(cursor, table, column, col_type):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    if column not in columns:
        print(f"➕ Agregando columna '{column}' a la tabla '{table}'...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")

def patch_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Agregar columnas a neuro_tokens
    add_column_if_not_exists(cursor, "neuro_tokens", "timestamp", "TEXT")
    add_column_if_not_exists(cursor, "neuro_tokens", "crypto", "TEXT DEFAULT 'NRN'")

    # Agregar columnas a neuro_nfts
    add_column_if_not_exists(cursor, "neuro_nfts", "timestamp", "TEXT")
    add_column_if_not_exists(cursor, "neuro_nfts", "crypto", "TEXT DEFAULT 'neuroNFT'")

    conn.commit()
    conn.close()
    print("✅ Parche aplicado correctamente.")

if __name__ == "__main__":
    patch_schema()
