import os
import json
import sqlite3
import numpy as np
from termux_backend.modules.modulo_symcontext.utils.embedding import obtener_embedding
from termux_backend.modules.modulo_tools.utils import get_settings # get_db_path

# DB_PATH = get_db_path()

# Cargar configuración del módulo NeuroBank
_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})
db_path = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db"))

def cargar_embeddings():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, input_text, embedding FROM context_entries WHERE embedding IS NOT NULL")
    datos = cursor.fetchall()
    conn.close()

    entradas = []
    for id_, texto, emb_str in datos:
        try:
            vect = np.array([float(x) for x in emb_str.split(",")])
            if vect.any():
                entradas.append((id_, texto, vect))
        except Exception as e:
            print(f"⚠️ Error cargando embedding ID {id_}: {e}")
    return entradas

def distancia_coseno(v1, v2):
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 1.0
    return 1 - np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def buscar_similares_emb(input_texto, top_n=6, embedding_ref=None):
    if embedding_ref is None:
        embedding_ref = np.array(obtener_embedding(input_texto))

    if not embedding_ref.any():
        print("⚠️ No se pudo obtener el embedding del texto.")
        return [], embedding_ref

    entradas = cargar_embeddings()
    if not entradas:
        print("⚠️ No hay entradas con embeddings para comparar.")
        return [], embedding_ref

    ranking = []
    for id_, texto, emb in entradas:
        dist = distancia_coseno(embedding_ref, emb)
        ranking.append((dist, id_, texto))

    ranking.sort()
    print(f"\n🔎 Más similares a: {input_texto}\n")
    for dist, id_, texto in ranking[:top_n]:
        print(f"⟪ Entrada #{id_} ⟫ — Distancia: {round(dist, 4)}")
        print("💬", texto[:190], "...\n")
    return ranking[:top_n], embedding_ref

if __name__ == "__main__":
    entrada = input("🧠 Ingresa texto de referencia:\n> ")
    buscar_similares_emb(entrada)
