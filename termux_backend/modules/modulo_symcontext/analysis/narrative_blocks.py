import os
import json
import sqlite3
import argparse
from termux_backend.modules.modulo_tools.utils import get_settings
from termux_backend.modules.modulo_symcontext.analysis.symbolic_analysis import analizar_narrativa

# Cargar configuración
_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})

# Diccionarios de íconos
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
emotion_icons = {
    "alegría": "😊", "tristeza": "😢", "enojo": "😠",
    "miedo": "😨", "calma": "😌", "confusión": "😵",
    "curiosidad": "🤔", "ninguna": "▫️", "otra": "🌀"
}

def normalizar(entrada, dic):
    if not entrada:
        return "❔"
    return dic.get(entrada.lower(), "❔")

def obtener_entradas():
    db = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db"))
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, purpose, identity_mode, tension, emotion, input_text
        FROM context_entries
        ORDER BY id ASC
    """)
    filas = cursor.fetchall()
    conn.close()
    entradas = []
    for row in filas:
        entradas.append({
            "id": row[0],
            "purpose": row[1],
            "identity_mode": row[2],
            "tension": row[3],
            "emotion": row[4],
            "texto": row[5]
        })
    return entradas

def generar_bloques_evolutivos():
    entradas = obtener_entradas()
    bloques = []
    bloque_actual = []
    anterior = None
    for e in entradas:
        clave_actual = (e["purpose"], e["identity_mode"], e["tension"], e["emotion"])
        if anterior is None or clave_actual == anterior:
            bloque_actual.append(e)
        else:
            bloques.append(bloque_actual)
            bloque_actual = [e]
        anterior = clave_actual
    if bloque_actual:
        bloques.append(bloque_actual)
    print("\n📚 BLOQUES EVOLUTIVOS SIMBÓLICOS")
    print("Cada bloque representa una etapa de coherencia interna\n")
    for idx, bloque in enumerate(bloques, 1):
        p, i, t, emo = bloque[0]["purpose"], bloque[0]["identity_mode"], bloque[0]["tension"], bloque[0]["emotion"]
        icon_p = normalizar(p, purpose_icons)
        icon_i = normalizar(i, identity_icons)
        icon_t = normalizar(t, tension_icons)
        icon_e = normalizar(emo, emotion_icons)
        print(f"──⟪ BLOQUE {idx} ⟫── {icon_p} {icon_i} {icon_t} {icon_e} → {p}/{i}/{t}/{emo}")
        for e in bloque:
            texto = e["texto"].strip().replace("\n", " ")
            print(f"#{str(e['id']).zfill(3)}: {texto[:100]}{'...' if len(texto)>100 else ''}")
        print("─" * 60)

def main(std=False):
    entradas = obtener_entradas()
    if std:
        generar_bloques_evolutivos()
    else:
        print("✨ Analizando bloques simbólicos con IA...\n")
        resultado = analizar_narrativa(entradas)
        print(resultado)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--std", action="store_true", help="Salida estandar")
    args = parser.parse_args()
    main(std=args.std)

