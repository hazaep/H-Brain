import os
import json
import sqlite3
import argparse

from termux_backend.modules.modulo_tools.utils import get_settings
from termux_backend.modules.modulo_symcontext.analysis import symbolic_analysis

# Cargar configuración
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

def generar_mapa_estandar():
    db = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db"))
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

def generar_mapa_ia():
    db = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db"))
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, purpose, identity_mode, tension
        FROM context_entries
        ORDER BY timestamp ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    entries = []
    for row in rows:
        id_, p, i, t = row
        entries.append({
            "id": id_,
            "purpose": p or "❔",
            "identity_mode": i or "❔",
            "tension": t or "❔"
        })

    print("✨ Línea de vida simbólica recibida. Enviando a análisis simbiótico IA...\n")
    try:
        resultado = symbolic_analysis.analizar_timeline(entries)
        print(resultado.strip())
    except Exception as e:
        print("❌ Error al generar análisis con IA:", e)

def main(std=False):
    if std:
        generar_mapa_estandar()
    else:
        generar_mapa_ia()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--std", action="store_true", help="Usar salida estándar (sin IA)")
    args = parser.parse_args()
    main(std=args.std)
