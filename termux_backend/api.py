# api.py

from flask import Flask, request, jsonify
from core import AutomationCore

app = Flask(__name__)
core = AutomationCore()

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    module = data.get("module")
    command = data.get("command")
    kwargs = data.get("args", {})

    result = core.execute_command(module, command, **kwargs)
    return jsonify(result)

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "H-Brain backend is running ✅"})

@app.route("/")
def home():
    return {"mensaje": "¡Hola desde H-Brain!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)
