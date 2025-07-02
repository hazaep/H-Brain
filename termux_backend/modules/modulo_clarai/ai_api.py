import os
import json
import requests
from termux_backend.modules.modulo_clarai.history import fetch_history
from termux_backend.modules.modulo_clarai.memory import (
    init_memory_db, load_top_memories, add_memory,
    delete_memory, rewrite_memory, search_memories
)

# Lee settings.json
def load_settings():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
    settings_path = os.path.join(project_root, "configs", "settings.json")
    with open(settings_path) as f:
        return json.load(f)

_cfg = load_settings()
API_KEY_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")), _cfg.get("deepseek_key_path", "configs/secrets/deepseek_key.txt"))
MODEL = _cfg.get("clarai_model", "deepseek-reasoner")
API_URL = _cfg.get("clarai_api_url", "https://api.deepseek.com/v1/chat/completions")
TEMPERATURE = _cfg.get("clarai_temperature", 0.7)
EXTRA_SLOTS = _cfg.get("clarai_extra_slots", 5)


def get_api_key():
    with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")), API_KEY_PATH), "r") as f:
        return f.read().strip()


def build_system_prompt(memories, search_results=[]):
    lines = [f"- [{m[0]}] Mem: {m[1]} Cat: {m[2]} Relevancia: {m[3]}" for m in memories]
    if search_results:
        lines += [f"- [F:{m[0]}] Mem: {m[1]} Cat: {m[2]} Relevancia: {m[3]}" for m in search_results]
    return f"""
Eres Clarai, asistente de IA creada por Hazael.
Especialización actual:
1.- Exploración teórica/IA
Reglas:
- Nunca afirmar tener conciencia
- Priorizar respuestas creativas
- Ajustar estilo según historial

2.- Gestionar el historial relevante (solo 1 comando por respuesta)
Comandos válidos:
- add: Mem: [resumen] Cat: [categoría] Relevancia: [X.X]
- del: [id]
- rew: [id] Mem: [nuevo] Cat: [nueva] Relevancia: [X.X]
- find: [palabras clave]
- esc:

# Memoria actual:
{chr(10).join(lines)}
"""


def send_message(username, conv_id, user_input):
    # Inicializar DBs
    hist_conn = init_history_db()
    mem_conn = init_memory_db()
    # fetch user_id
    from termux_backend.modules.modulo_clarai.history import get_or_create_user
    user_id = get_or_create_user(hist_conn, username)

    # Obtener y limitar historial
    history = fetch_history(hist_conn, conv_id)[-8:]

    # Cargar memorias y buscar si aplica
    memories = load_top_memories(mem_conn, user_id)
    search_results = []
    if user_input.lower().startswith("find:"):
        keyword = user_input.split("find:",1)[1].strip()
        search_results = search_memories(mem_conn, user_id, keyword, EXTRA_SLOTS)

    prompt = build_system_prompt(memories, search_results)
    messages = [{"role":"system","content":prompt}] + history

    headers = {'Authorization':f'Bearer {get_api_key()}','Content-Type':'application/json'}
    data = {'model':MODEL,'messages':messages,'temperature':TEMPERATURE}

    resp = requests.post(API_URL, headers=headers, json=data)
    if resp.status_code != 200:
        return f"[❌ Error {resp.status_code}] {resp.text}"

    raw = resp.json()['choices'][0]['message']['content']
    try:
        parsed = json.loads(raw) if raw.strip().startswith("{") else {"respuesta":raw,"comando":""}
    except json.JSONDecodeError:
        return f"[❌ JSON inválido]\n{raw}"

    respuesta = parsed.get("respuesta","")
    comando = parsed.get("comando","")
    from termux_backend.modules.modulo_clarai.memory import process_memory_command
    cmd = process_memory_command(comando)
    if cmd:
        action = cmd.get("action")
        if action == "add":
            add_memory(mem_conn, user_id, cmd["summary"], cmd["category"], cmd["relevance"])
        elif action == "del":
            delete_memory(mem_conn, user_id, cmd["id"])
        elif action == "rew":
            rewrite_memory(mem_conn, user_id, cmd["id"], cmd.get("summary"), cmd.get("category"), cmd.get("relevance"))
    # Guardar mensaje de assistant
    from termux_backend.modules.modulo_clarai.history import add_message as _add_msg
    _add_msg(hist_conn, conv_id, 'assistant', respuesta)
    return respuesta
