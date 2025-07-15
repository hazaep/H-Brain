import os
import sqlite3
from termux_backend.modules.modulo_tools.utils import get_settings
from termux_backend.modules.modulo_symcontext.utils.semantic_search import buscar_similares_emb
from termux_backend.modules.modulo_symcontext.analysis.symbolic_analysis import analizar_similares

# Cargar configuración del módulo SymContext
_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})

def encontrar_relaciones_semanticas(texto_referencia):
    db_path = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db"))
    base_entry = None

    # 1. Buscar en la DB si existe una entrada que contenga ese texto
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, input_text FROM context_entries WHERE input_text LIKE ? ORDER BY timestamp DESC LIMIT 1",
        ('%' + texto_referencia + '%',)
    )
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        base_entry = {"id": resultado[0], "texto": resultado[1]}
        print(f"🎯 Entrada encontrada en DB: #{base_entry['id']}")
    else:
        # Si no está registrada, se crea una entrada base dummy
        base_entry = {"id": 0, "texto": texto_referencia}
        print("📎 Fragmento no encontrado en DB. Usando texto como entrada base.")

    print("🔧 Generando embedding y buscando relaciones simbólicas...")
    similares, _ = buscar_similares_emb(base_entry["texto"], top_n=5)

    if not similares:
        print("⚠️ No se encontraron entradas similares.")
        return

    similares_fmt = [{"id": id_, "texto": texto} for _, id_, texto in similares]

    print("\n🧠 Análisis simbiótico enriquecido por IA:\n")
    print(analizar_similares(base_entry, similares_fmt))


def main():
    texto = input("🧶 Fragmento del texto base a analizar:\n> ").strip()
    if texto:
        encontrar_relaciones_basicas(texto)
    else:
        print("⚠️ No ingresaste texto de referencia.")

if __name__ == "__main__":
    main()
