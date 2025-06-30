import sqlite3
from termux_backend.modules.modulo_ai.ai_router import embed
from termux_backend.modules.modulo_tools.utils import get_db_path

DB_PATH = get_db_path()

def obtener_embedding(texto):
    texto = texto.strip()
    if not texto:
        print("⚠️ Texto vacío, no se puede procesar.")
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT embedding FROM context_entries WHERE input_text = ?", (texto,))
        resultado = cursor.fetchone()

        if resultado and resultado[0]:
            print("🧠 Embedding existente encontrado en base de datos.")
            embedding = [float(x) for x in resultado[0].split(",")]
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
        return embedding

    except Exception as e:
        print("❌ Error inesperado:", e)
    finally:
        conn.close()

    return []
