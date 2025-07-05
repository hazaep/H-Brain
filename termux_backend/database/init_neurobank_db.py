import sqlite3
import os
import json

SETTINGS_PATH = os.path.expanduser("~/H-Brain/configs/settings.json")
with open(SETTINGS_PATH, "r") as f:
    settings = json.load(f)

DB_PATH = os.path.expanduser("~/H-Brain/" + settings.get("neurobank_db_path", "termux_backend/database/naurobank_vault.db"))

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS neuro_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module TEXT,
        action TEXT,
        amount INTEGER,
        input_id INTEGER,
        crypto TEXT,
        metadata TEXT,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS neuro_nfts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_id INTEGER,
        title TEXT,
        crypto TEXT,
        metadata TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas de NeuroBank creadas o actualizadas.")

if __name__ == "__main__":
    create_tables()
