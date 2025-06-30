# analysis/graph_builder.py

import os
import sqlite3
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from termux_backend.modules.modulo_tools.utils import get_settings, get_db_path
from termux_backend.modules.modulo_symcontext.utils.embedding import obtener_embedding
#from utils.embedding import obtener_embedding

def cargar_entradas_con_embeddings():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, input_text, embedding FROM context_entries WHERE embedding IS NOT NULL")
    entradas = []
    for id_, texto, emb_str in cursor.fetchall():
        try:
            emb = np.array([float(x) for x in emb_str.split(",")])
            entradas.append((id_, texto, emb))
        except Exception as e:
            print(f"⚠️ Error cargando embedding de ID {id_}: {e}")
            continue
    conn.close()
    return entradas

def distancia_coseno(v1, v2):
    num = np.dot(v1, v2)
    den = np.linalg.norm(v1) * np.linalg.norm(v2)
    return 1 - (num / den)

def construir_grafo(entradas, umbral=0.25):
    G = nx.Graph()
    for id_, texto, _ in entradas:
        G.add_node(id_, label=texto[:50] + "..." if len(texto) > 50 else texto)
    for i in range(len(entradas)):
        id1, _, emb1 = entradas[i]
        for j in range(i + 1, len(entradas)):
            id2, _, emb2 = entradas[j]
            dist = distancia_coseno(emb1, emb2)
            if dist < umbral:
                G.add_edge(id1, id2, weight=1 - dist)
    return G

def visualizar_grafo(G, output_path):
    if G.number_of_nodes() == 0:
        print("⚠️ No hay nodos para graficar.")
        return

    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_node_attributes(G, "label")
    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="skyblue", alpha=0.8)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    plt.title("Grafo de Pensamientos Similares (SymContext)", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def generar_grafo_contextual(nombre="grafo.png", umbral=0.25):
    config = get_settings()
    output_dir = config.get("graph_output_dir", "./grafo_salidas")
    os.makedirs(output_dir, exist_ok=True)

    entradas = cargar_entradas_con_embeddings()
    if not entradas:
        print("⚠️ No hay entradas con embeddings para generar el grafo.")
        return None

    G = construir_grafo(entradas, umbral=umbral)
    output_path = os.path.join(output_dir, nombre)
    visualizar_grafo(G, output_path)
    return output_path

if __name__ == "__main__":
    ruta = generar_grafo_contextual()
    if ruta:
        print(f"✅ Grafo generado en:\n{ruta}")
