import sqlite3
from termux_backend.modules.modulo_tools.utils import get_db_path

def encontrar_relaciones_basicas(texto_referencia):
    db = get_db_path()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # 1) Buscar entrada base
    cursor.execute(
        "SELECT id, purpose, identity_mode, tension FROM context_entries "
        "WHERE input_text LIKE ? ORDER BY timestamp DESC LIMIT 1",
        ('%' + texto_referencia + '%',)
    )
    base = cursor.fetchone()
    if not base:
        print("❌ Entrada no encontrada.")
        conn.close()
        return

    ref_id, ref_purpose, ref_identity, ref_tension = base
    print(f"🔍 Analizando relaciones con entrada #{ref_id}")
    print(f"🎯 Propósito: {ref_purpose}, 👤 Identidad: {ref_identity}, 🔥 Tensión: {ref_tension}\n")

    # 2) Buscar entradas que compartan al menos un campo simbólico
    cursor.execute(
        "SELECT id, input_text, purpose, identity_mode, tension FROM context_entries "
        "WHERE id != ? AND (purpose = ? OR identity_mode = ? OR tension = ?) "
        "ORDER BY timestamp DESC LIMIT 10",
        (ref_id, ref_purpose, ref_identity, ref_tension)
    )
    relacionados = cursor.fetchall()
    conn.close()

    if relacionados:
        for id_, texto, purpose, identity, tension in relacionados:
            print(f"───⟪ Entrada #{id_} ⟫───")
            print("💬", texto[:160] + ("..." if len(texto) > 160 else ""))
            print(f"🎯 {purpose} | 👤 {identity} | 🔥 {tension}")
            print("────────────────────────────\n")
    else:
        print("⚠️ No se encontraron relacionadas simbólicamente.")

def main():
    texto = input("🧶 Fragmento del texto base a analizar:\n> ").strip()
    if texto:
        encontrar_relaciones_basicas(texto)
    else:
        print("⚠️ No ingresaste texto de referencia.")

if __name__ == "__main__":
    main()

