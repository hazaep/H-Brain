import os
import sqlite3
from termux_backend.modules.modulo_tools.utils import get_settings
from termux_backend.modules.modulo_clarai import embedding_tools

# Configuración
_cfg = get_settings()
CLARAI_CFG = _cfg.get("clarai", {})
HIST_DB = os.path.expanduser(CLARAI_CFG.get("history_db_path", "termux_backend/database/ai_history.db"))
MEM_DB = os.path.expanduser(CLARAI_CFG.get("memory_db_path", "termux_backend/database/clarai_memory.db"))

# Crear tabla message_embeddings si no existe
def patch_message_embeddings():
    conn = sqlite3.connect(HIST_DB)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS message_embeddings (
                message_id INTEGER PRIMARY KEY,
                role TEXT NOT NULL,
                embedding BLOB NOT NULL,
                FOREIGN KEY(message_id) REFERENCES messages(id)
            );
        """)
    print("✅ Tabla 'message_embeddings' verificada.")

    # Cargar mensajes y generar embeddings faltantes
    cur = conn.execute("SELECT id, role, content FROM messages")
    for msg_id, role, content in cur.fetchall():
        # Evitar duplicados
        exists = conn.execute("SELECT 1 FROM message_embeddings WHERE message_id=?", (msg_id,)).fetchone()
        if exists:
            continue
        emb = embedding_tools.generate_embedding(content)
        embedding_tools.insert_message_embedding(conn, msg_id, role, emb)
        print(f"🧠 Embedding generado para mensaje ID {msg_id} ({role})")
    conn.close()

# Crear tabla memory_embeddings si no existe
def patch_memory_embeddings():
    conn = sqlite3.connect(MEM_DB)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_embeddings (
                memory_id INTEGER PRIMARY KEY,
                embedding BLOB NOT NULL,
                FOREIGN KEY(memory_id) REFERENCES memories(id)
            );
        """)
    print("✅ Tabla 'memory_embeddings' verificada.")

    # Cargar memorias y generar embeddings faltantes
    cur = conn.execute("SELECT id, summary FROM memories")
    for mem_id, summary in cur.fetchall():
        exists = conn.execute("SELECT 1 FROM memory_embeddings WHERE memory_id=?", (mem_id,)).fetchone()
        if exists:
            continue
        emb = embedding_tools.generate_embedding(summary)
        embedding_tools.insert_memory_embedding(conn, mem_id, emb)
        print(f"🧠 Embedding generado para memoria ID {mem_id}")
    conn.close()

# === Ejecutar todo ===
if __name__ == "__main__":
    patch_message_embeddings()
    patch_memory_embeddings()
    print("\n✅ Parchado completo.")
