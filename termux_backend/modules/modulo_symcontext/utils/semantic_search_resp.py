import sqlite3
import numpy as np
from termux_backend.modules.modulo_symcontext.utils.embedding import obtener_embedding
from termux_backend.modules.modulo_tools.utils import get_db_path

DB_PATH = get_db_path()

def cargar_embeddings():
    conn = sqlite3.connect(DB_PATH)
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

def buscar_similares(input_texto, top_n=5):
    ref_emb = np.array(obtener_embedding(input_texto))
    if not ref_emb.any():
        print("⚠️ No se pudo obtener el embedding del texto.")
        return

    entradas = cargar_embeddings()
    if not entradas:
        print("⚠️ No hay entradas con embeddings para comparar.")
        return

    ranking = []
    for id_, texto, emb in entradas:
        dist = distancia_coseno(ref_emb, emb)
        ranking.append((dist, id_, texto))

    ranking.sort()
    print(f"\n🔎 Más similares a: {input_texto}\n")
    for dist, id_, texto in ranking[:top_n]:
        print(f"⟪ Entrada #{id_} ⟫ — Distancia: {round(dist, 4)}")
        print("💬", texto[:150], "...\n")

def buscar_similares_emb(entrada_texto):
    buscar_similares(entrada_texto)

if __name__ == "__main__":
    entrada = input("🧠 Ingresa texto de referencia:\n> ")
    buscar_similares(entrada)
