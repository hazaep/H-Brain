import os
import json
import sqlite3
from datetime import datetime
from termux_backend.modules.modulo_symcontext.utils.classify_input import clasificar_input
from termux_backend.modules.modulo_symcontext.utils.semantic_search import buscar_similares_emb
from termux_backend.modules.modulo_symcontext.analysis.graph_builder import generar_grafo_contextual
from termux_backend.modules.modulo_tools.utils import get_settings  #, get_db_path, get_log_path

# DB_PATH = get_db_path()
# LOG_PATH = get_log_path("user_inputs.log")

# Cargar configuración del módulo SymContext
_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})
DB_PATH = os.path.expanduser(_cfg.get("sym_db_path", "termux_backend/database/context.db"))


tags = ""

def tag_input(user_input):
    print("🧠 Clasificando entrada...")
    clasificacion = clasificar_input(user_input)

    if clasificacion:
        print("✅ Clasificación sugerida:")
        for clave, valor in clasificacion.items():
            print(f"{clave}: {valor}")
#        if input("¿Aceptar estas categorías? (s/n): ").lower() == "s":
        return (
            clasificacion['purpose'],
            clasificacion['identity_mode'],
            clasificacion['tension'],
            clasificacion['tags'],
        )

#    print("✍️ Ingresá manualmente:")
#    purpose = input("¿Propósito del input (explorar, desahogo, insight, pregunta, otro)?: ")
#    identity = input("¿Desde qué yo hablás? (niño, observador, estratega, instintivo, otro): ")
#    tension = input("¿Qué tipo de tensión hay? (mental, emocional, creativa, ninguna, otra)?: ")
#    tags = input("Etiquetas sueltas (opcional, coma separadas): ")
#    return purpose, identity, tension, tags

def log_input(texto):
    with open(LOG_PATH, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {texto}\n")

def save_input(texto, generar_grafo=True):
    if not texto.strip():
        print("⚠️ Entrada vacía. No se guardó nada.")
        return None  # ← Esto evita que retorne None sin control

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Clasificación del input
        purpose, identity_mode, tension, tags = tag_input(texto)

        # Obtener embedding, similares y convertir a string
        similares, embedding = buscar_similares_emb(texto)
        embedding_str = ",".join(str(x) for x in embedding)

        # Insertar en base de datos
        cursor.execute("""
            INSERT INTO context_entries (input_text, purpose, identity_mode, tension, tags, embedding)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (texto, purpose, identity_mode, tension, tags, embedding_str))
        conn.commit()

        # Obtener ID recién insertado
        cursor.execute("SELECT last_insert_rowid()")
        last_id = cursor.fetchone()[0]
        print(f"🆔 Entrada registrada con ID #{last_id}")

        # Generar grafo si corresponde
        path_grafo = None
        if generar_grafo:
            path_grafo = generar_grafo_contextual()
            print(f"📍 Gráfico actualizado en:\n{path_grafo}")

        # Retornar diccionario con datos clave
        return {
            "id": last_id,
            "texto": texto,
            "purpose": purpose,
            "identity_mode": identity_mode,
            "tension": tension,
            "tags": tags,
            "grafo_path": path_grafo
        }

    except Exception as e:
        print(f"❌ Error al guardar la entrada: {e}")
        return None

    finally:
        conn.close()

#if __name__ == "__main__":
#    texto = input("🗣️ ¿Qué quieres registrar ahora en SymContext?:\n> ")
#    save_input(texto)
