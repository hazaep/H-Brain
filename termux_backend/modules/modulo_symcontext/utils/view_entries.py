import sqlite3
from termux_backend.modules.modulo_tools.utils import get_db_path

def mostrar_entradas(filtro_col=None, filtro_val=None):
    db = get_db_path()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    if filtro_col and filtro_val:
        query = (
            "SELECT id, input_text, timestamp, purpose, identity_mode, tension, tags "
            "FROM context_entries WHERE {} = ? ORDER BY timestamp DESC"
        ).format(filtro_col)
        cursor.execute(query, (filtro_val,))
    else:
        cursor.execute(
            "SELECT id, input_text, timestamp, purpose, identity_mode, tension, tags "
            "FROM context_entries ORDER BY timestamp DESC"
        )

    entradas = cursor.fetchall()
    conn.close()

    if entradas:
        for id_, texto, timestamp, purpose, identity, tension, tags in entradas:
            print(f"───⟪ Entrada #{id_} ⟫───")
            print("🕛", timestamp)
            print("💬", texto)
            print("🎯 Propósito:", purpose)
            print("🧬 Identidad:", identity)
            print("🔥 Tensión:", tension)
            print("🏷️ Etiquetas:", tags)
            print("──────────────────────\n")
    else:
        print("⚠️ No se encontraron registros con ese filtro.")

def main():
    print("🧭 Filtros disponibles: [purpose, identity_mode, tension, tags]")
    filtro_col = input("¿Filtrar por cuál columna? (Enter para ver todo): ").strip() or None
    filtro_val = None
    if filtro_col:
        filtro_val = input(f"Ingresá el valor de '{filtro_col}': ").strip()
    mostrar_entradas(filtro_col, filtro_val)

if __name__ == "__main__":
    main()
