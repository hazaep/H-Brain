import os
import json
import sqlite3
import argparse

from termux_backend.modules.modulo_tools.utils import get_settings
from termux_backend.modules.modulo_symcontext.analysis import symbolic_analysis

# Configuración global
_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})

def detectar_transiciones_estandar():
    db = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db"))
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

def detectar_transiciones_ia():
    db = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db"))
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, purpose, identity_mode, tension
        FROM context_entries
        ORDER BY id ASC
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

    print("✨ Secuencia simbólica recibida. Enviando a IA para análisis de transiciones...\n")
    try:
        resultado = symbolic_analysis.analizar_transiciones(entries)
        print(resultado.strip())
    except Exception as e:
        print("❌ Error al generar análisis con IA:", e)

def main(std=False):
    if std:
        detectar_transiciones_estandar()
    else:
        detectar_transiciones_ia()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--std", action="store_true", help="Usar vista estándar sin IA")
    args = parser.parse_args()
    main(std=args.std)
