import os
import json
import sqlite3
from termux_backend.modules.modulo_tools.utils import get_settings # get_db_path

# Cargar configuración del módulo SymContext
_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})

def detectar_transiciones():
    db = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db")) # get_db_path()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, purpose, identity_mode, tension
        FROM context_entries
        ORDER BY id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    prev = None
    print("\n🚧 TRANSICIONES SIGNIFICATIVAS DETECTADAS")
    for id_, p, i, t in rows:
        if prev:
            cambios = []
            if p != prev[1]:
                cambios.append(f"🧭 Propósito: {prev[1]} → {p}")
            if i != prev[2]:
                cambios.append(f"🧍 Identidad: {prev[2]} → {i}")
            if t != prev[3]:
                cambios.append(f"💢 Tensión: {prev[3]} → {t}")
            if cambios:
                print(f"\n⟿ Transición alrededor del ID #{str(id_).zfill(3)}")
                for c in cambios:
                    print("    " + c)
                print("─" * 30)
        prev = (id_, p, i, t)

def main():
    detectar_transiciones()

if __name__ == "__main__":
    main()
