import sqlite3
from termux_backend.modules.modulo_tools.utils import get_db_path

def init_neurobank_schema():
    db_path = get_db_path()
    with open(__file__.replace("__init__.py", "schema_neurobank.sql"), "r") as f:
        schema_sql = f.read()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("✅ Tablas de NeuroBank inicializadas.")
