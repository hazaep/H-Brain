import sqlite3
from termux_backend.modules.modulo_tools.utils import get_db_path

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

def normalizar(entrada, dic):
    return dic.get(entrada.lower(), "❔")

def generar_bloques_evolutivos():
    db = get_db_path()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, purpose, identity_mode, tension, input_text
        FROM context_entries
        ORDER BY id ASC
    """)
    entradas = cursor.fetchall()
    conn.close()

    bloques = []
    bloque_actual = []
    anterior = None

    for id_, p, i, t, texto in entradas:
        clave_actual = (p, i, t)
        if anterior is None or clave_actual == anterior:
            bloque_actual.append((id_, p, i, t, texto))
        else:
            bloques.append(bloque_actual)
            bloque_actual = [(id_, p, i, t, texto)]
        anterior = clave_actual

    if bloque_actual:
        bloques.append(bloque_actual)

    print("\n📚 BLOQUES EVOLUTIVOS SIMBÓLICOS")
    print("Cada bloque representa una etapa de coherencia interna\n")
    for idx, bloque in enumerate(bloques, 1):
        p, i, t = bloque[0][1], bloque[0][2], bloque[0][3]
        icon_p = normalizar(p, purpose_icons)
        icon_i = normalizar(i, identity_icons)
        icon_t = normalizar(t, tension_icons)
        print(f"──⟪ BLOQUE {idx} ⟫── {icon_p} {icon_i} {icon_t} → {p}/{i}/{t}")
        for id_, _, _, _, texto in bloque:
            frase = texto.strip().replace("\n", " ")
            print(f"#{str(id_).zfill(3)}: {frase[:100]}{'...' if len(frase)>100 else ''}")
        print("─" * 60)

def main():
    generar_bloques_evolutivos()

if __name__ == "__main__":
    main()
