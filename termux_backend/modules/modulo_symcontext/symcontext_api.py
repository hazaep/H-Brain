# termux_backend/modules/modulo_symcontext/symcontext_api.py

from flask import Flask, request, jsonify
from utils.input import save_input
from analysis.timeline_map import generar_timeline
from analysis.graph_builder import generar_grafo_contextual
from utils.semantic_search import buscar_similares_emb

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "🧠 SymContext API en funcionamiento",
        "endpoints": {
            "POST /registrar": "Registrar nueva entrada",
            "GET /timeline": "Obtener timeline",
            "GET /grafo": "Ruta del grafo actual",
            "GET /similares?texto=...": "Buscar pensamientos similares"
        }
    })

@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.get_json()
    texto = data.get("texto", "").strip()

    if not texto:
        return jsonify({"error": "Texto vacío"}), 400

    resultado = save_input(texto)
    if resultado:
        return jsonify({"status": "ok", "resultado": resultado}), 200
    else:
        return jsonify({"error": "Error al guardar"}), 500

@app.route("/timeline", methods=["GET"])
def timeline():
    try:
        timeline = generar_timeline()
        return jsonify({"timeline": timeline})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/grafo", methods=["GET"])
def grafo():
    try:
        grafo_path = generar_grafo_contextual()
        return jsonify({"grafo_path": grafo_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/similares", methods=["GET"])
def similares():
    texto = request.args.get("texto", "")
    if not texto:
        return jsonify({"error": "Falta el parámetro 'texto'"}), 400

    try:
        resultados = buscar_similares_emb(texto)
        return jsonify({"similares": resultados})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
