import os
import json
import math
import sqlite3
from termux_backend.modules.modulo_ai.ai_router import embed
from termux_backend.modules.modulo_tools.utils import get_settings
from termux_backend.modules.modulo_tools.bank_metadata import metadata_token

# Cargar configuración del módulo NeuroBank
_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})

def cosine_similarity(vec1, vec2):
    dot = sum(a*b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a*a for a in vec1))
    norm2 = math.sqrt(sum(b*b for b in vec2))
    return dot / (norm1 * norm2 + 1e-9)

def obtener_embedding(texto):
    texto = texto.strip()
    if not texto:
        print("⚠️ Texto vacío, no se puede procesar.")
        return []

    db = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db"))
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT embedding FROM context_entries WHERE input_text = ?", (texto,))
        resultado = cursor.fetchone()

        if resultado and resultado[0]:
            print("🧠 Embedding existente encontrado en base de datos.")
            embedding = [float(x) for x in resultado[0].split(",")]
            metadata_token(
                module="SymContext",
                action=f"Embedding: {texto}",
                funcion="termux_backend.modules.modulo_symcontext.utils.embedding : obtener_embedding",
                entrada=texto,
                salida=f"Embedding Len: {len(embedding)}",
                input_id="N/A",
                crypto="SYNAP"
            )
            return embedding

        print("✨ Generando nuevo embedding...")
        embedding = embed(texto)
        if not embedding:
            print("❌ No se pudo generar embedding.")
            return []

        embedding_str = ",".join(str(x) for x in embedding)
        cursor.execute("UPDATE context_entries SET embedding = ? WHERE input_text = ?", (embedding_str, texto))
        conn.commit()
        print("💾 Embedding generado y guardado.")
        metadata_token(
            module="SymContext",
            action=f"Embedding: {texto}",
            funcion="termux_backend.modules.modulo_symcontext.utils.embedding : obtener_embedding",
            entrada=texto,
            salida=f"Embedding Len: {len(embedding)}",
            input_id="N/A",
            crypto="SYNAP"
        )
        return embedding

    except Exception as e:
        print("❌ Error inesperado:", e)
    finally:
        conn.close()

    return []
