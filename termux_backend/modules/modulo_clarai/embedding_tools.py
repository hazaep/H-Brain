import numpy as np
import sqlite3
import os
from openai import OpenAI
from termux_backend.modules.modulo_tools.utils import get_settings

# === CONFIGURACIÓN ===

_cfg = get_settings()
clarai_cfg = _cfg.get("clarai", {})
EMB_MODEL = clarai_cfg.get("embedding_model", "text-embedding-3-small")
EMB_API_URL = clarai_cfg.get("embedding_api_url", "https://api.openai.com/v1")
EMB_KEY_PATH = os.path.expanduser(clarai_cfg.get("embedding_key_path", "configs/secrets/openai_key.txt"))

# === Cliente de Embeddings ===

def get_embedding_client():
    key = open(EMB_KEY_PATH).read().strip()
    return OpenAI(api_key=key, base_url=EMB_API_URL)

def generate_embedding(text):
    client = get_embedding_client()
    response = client.embeddings.create(
        model=EMB_MODEL,
        input=text
    )
    return response.data[0].embedding

# === Conversión de BLOBs ===

def to_blob(embedding):
    return np.array(embedding, dtype=np.float32).tobytes()

def from_blob(blob):
    return np.frombuffer(blob, dtype=np.float32)

# === Similitud por Coseno ===

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# === Inserción de Embeddings ===

def insert_message_embedding(conn, message_id, role, embedding):
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO message_embeddings (message_id, role, embedding)
            VALUES (?, ?, ?)
        """, (message_id, role, to_blob(embedding)))

def insert_memory_embedding(conn, memory_id, embedding):
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO memory_embeddings (memory_id, embedding)
            VALUES (?, ?)
        """, (memory_id, to_blob(embedding)))

# === Búsqueda de Mensajes Similares ===

def search_similar_message_embeddings(conn, target_emb, top_n=4):
    cur = conn.execute("SELECT message_id, role, embedding FROM message_embeddings")
    results = []
    for row in cur.fetchall():
        emb = from_blob(row[2])
        sim = cosine_similarity(target_emb, emb)
        results.append((sim, row[0], row[1]))
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_n]

# === Búsqueda de Memorias Similares ===

def search_similar_memory_embeddings(conn, target_emb, top_n=4):
    cur = conn.execute("SELECT memory_id, embedding FROM memory_embeddings")
    results = []
    for row in cur.fetchall():
        emb = from_blob(row[1])
        sim = cosine_similarity(target_emb, emb)
        results.append((sim, row[0]))
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_n]
