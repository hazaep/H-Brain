import os
import sqlite3
import re
from datetime import datetime
from termux_backend.modules.modulo_tools.utils import get_settings
from termux_backend.modules.modulo_symcontext.utils.semantic_search import buscar_similares_emb
from termux_backend.modules.modulo_symcontext.analysis.symbolic_analysis import analizar_similares

# Cargar configuración del módulo SymContext
_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})

def sanitizar_nombre(nombre):
    """Convierte texto a un nombre de archivo válido"""
    nombre = nombre.lower().strip()
    nombre = re.sub(r"[^a-z0-9]+", "_", nombre)
    return nombre[:40] or "entrada"

def guardar_en_archivo(texto, similares, contenido):
    contador = 0
    related_dir = SYM_CFG.get("related_output_dir", "./related_salidas")
    os.makedirs(related_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
    nombre_base = sanitizar_nombre(texto)
    filename = f"{nombre_base}_{timestamp}.md"
    ruta = os.path.join(related_dir, filename)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# 🧠 Análisis simbiótico\n")
        f.write(f"🕓 Generado: {timestamp}\n\n")
        for i in similares:
            contador += 1
            f.write(f" Entrada #{contador}\n{i}\n")
        f.write(contenido)
    print(f"\n\n📁 Analisis guardado en: {ruta}")

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
        base_entry = {"id": 0, "texto": texto_referencia}
        print("📎 Fragmento no encontrado en DB. Usando texto como entrada base.")

    print("🔧 Generando embedding y buscando relaciones simbólicas...")
    similares, _ = buscar_similares_emb(base_entry["texto"], top_n=5)

    if not similares:
        print("⚠️ No se encontraron entradas similares.")
        return

    similares_fmt = [{"id": id_, "texto": texto} for _, id_, texto in similares]

    print("\n🧠 Análisis simbiótico enriquecido por IA:\n")
    resultado = analizar_similares(base_entry, similares_fmt)
    print(resultado)

    guardar_en_archivo(base_entry["texto"], similares_fmt, resultado)


def main():
    texto = input("🧶 Fragmento del texto base a analizar:\n> ").strip()
    if texto:
        encontrar_relaciones_basicas(texto)
    else:
        print("⚠️ No ingresaste texto de referencia.")

if __name__ == "__main__":
    main()
