import sqlite3
from termux_backend.modules.modulo_tools.utils import get_db_path

DB_PATH = get_db_path()

def crear_tablas_neurobank():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla para tokens
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS neuro_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            module TEXT,
            action TEXT,
            amount INTEGER,
            input_id INTEGER,
            metadata TEXT
        );
    """)

    # Tabla para NFTs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS neuro_nfts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            input_id INTEGER,
            title TEXT,
            metadata TEXT
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas de NeuroBank creadas o actualizadas.")

if __name__ == "__main__":
    crear_tablas_neurobank()
