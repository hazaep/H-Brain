import os
import json
import sqlite3
from termux_backend.modules.modulo_tools.utils import get_settings # get_db_path

# Cargar configuración del módulo SymContext
_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})

# Íconos simbólicos
purpose_icons = {
    "explorar": "🔍", "insight": "💡", "desahogo": "💬",
    "pregunta": "❓", "otro": "🌀"
}
identity_icons = {
    "observador": "👁️", "estratega": "♟️",
    "instintivo": "🔥", "niño": "🧒", "filósofo": "📚",
    "explorador": "🧭", "otro": "👤"
}
tension_icons = {
    "mental": "🧠", "emocional": "💓", "creativa": "🎨",
    "somatica": "🧘", "ninguna": "☁️", "otra": "🌀"
}

def normalizar(valor, diccionario):
    return diccionario.get(valor.lower(), "❔")

def generar_mapa():
    db = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db")) #get_db_path()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, purpose, identity_mode, tension
        FROM context_entries
        ORDER BY timestamp ASC
    """)
    entradas = cursor.fetchall()
    conn.close()

    print("\n📈 LINEA DE VIDA SIMBÓLICA (ID → Propósito | Identidad | Tensión):\n")
    for id_, p, i, t in entradas:
        icon_p = normalizar(p, purpose_icons)
        icon_i = normalizar(i, identity_icons)
        icon_t = normalizar(t, tension_icons)
        print(f"#{str(id_).zfill(3)} | {icon_p} {icon_i} {icon_t}  → {p}/{i}/{t}")

def main():
    generar_mapa()

if __name__ == "__main__":
    main()
