from utils.embedding import cosine_similarity
import json
import sqlite3
# Cargar 2 embeddings de la base
conn = sqlite3.connect("termux_backend/database/context.db")
cursor = conn.cursor()
cursor.execute("SELECT embedding FROM context_entries WHERE id IN (4, 5)")
rows = cursor.fetchall()
conn.close()

emb1 = json.loads(rows[0][0])
emb2 = json.loads(rows[1][0])

sim = cosine_similarity(emb1, emb2)
print(f"🔬 Similitud entre ID 4 y 5: {sim:.4f}")
