import os, json, requests
from termux_backend.modules.modulo_clarai import history, memory
# si quieres usar el router de modulo_ai:
# from termux_backend.modules.modulo_ai.ai_router import route_request

_cfg = json.load(open(os.path.expanduser("~/H-Brain/configs/settings.json")))
API_URL   = _cfg["clarai_api_url"]
MODEL     = _cfg["clarai_model"]
TEMP      = _cfg["clarai_temperature"]
KEY_PATH  = _cfg["deepseek_key_path"]


#os.path.join(_cfg["base_dir"],

def get_api_key():
    return open(os.path.expanduser(KEY_PATH)).read().strip()

def build_system_prompt(username,memories, search_results=None):
    lines = []
    for m in memories:
        lines.append(f"- [{m[0]}] Mem: {m[1]} Cat: {m[2]} Relevancia: {m[3]}")
    if search_results:
        for m in search_results:
            lines.append(f"- [F:{m[0]}] Mem: {m[1]} Cat: {m[2]} Relevancia: {m[3]}")
    return f"""
Eres Clarai, asistente de IA creada por Hazael.
Usuario: {username}

Especialización actual:
1.- Exploración teórica/IA
Reglas:
- Ajustar estilo según historial

2.- Gestionar el historial relevante según tu criterio (solo 1 comando por respuesta)

Comandos válidos:
- add: Mem: [resumen] Cat: [categoría] Relevancia: [X.X]  # Agregar
- del: [id]                                                # Eliminar
- rew: [id] Mem: [...] Cat: [...] Relevancia: [X.X]        # Modificar
- find: [palabras clave]                                   # Buscar recuerdos relacionados
- esc:                                                     # Ninguna acción

🟡 IMPORTANTE: #Esto es para la logica de los comandos
Siempre responde en formato JSON con dos claves:
{{
  "respuesta": "Tu mensaje al usuario",
  "comando": "comando_en_formato"
}}

# Memoria actual:
{chr(10).join(lines)}
""".strip()


def send_message(username, conv_id, user_input):
    # inicializar DBs
    conn     = history.init_history_db()
    mem_conn = memory.init_memory_db()
    user_id  = history.get_or_create_user(conn, username)

    # guardar input
    history.add_message(conn, conv_id, 'user', user_input)

    # historial limitado
    history_msgs = history.fetch_history(conn, conv_id)

    # memoria + búsqueda
    top = memory.load_top_memories(mem_conn, user_id)
    search = []
    if user_input.lower().startswith("find:"):
        kw = user_input.split(":",1)[1].strip()
        search = memory.search_memories(mem_conn, user_id, kw)

    # preparar prompt
    system = build_system_prompt(username, top, search)
    messages = [{"role":"system","content":system}] + history_msgs

    # enviar a la API (o a router si usas modulo_ai)
    payload = {'model':MODEL,'messages':messages,'temperature':TEMP}
    headers = {'Authorization':f'Bearer {get_api_key()}', 'Content-Type':'application/json'}
    resp = requests.post(API_URL, headers=headers, json=payload)

    if resp.status_code != 200:
        return f"[Error {resp.status_code}] {resp.text}"

    content = resp.json()['choices'][0]['message']['content']
    # parsear respuesta
    if not content.strip().startswith("{"):
        history.add_message(conn, conv_id, 'assistant', content)
        return content

    data = json.loads(content)
    answer = data.get("respuesta","")
    cmd = memory.process_memory_command(data.get("comando",""))

    # ejecutar comando de memoria
    if cmd:
        action = cmd["action"]
        if action=="add":
            memory.add_memory(mem_conn, user_id, cmd["summary"], cmd["category"], cmd["relevance"])
        elif action=="del":
            memory.delete_memory(mem_conn, user_id, cmd["id"])
        elif action=="rew":
            memory.rewrite_memory(mem_conn, user_id, cmd["id"],
                                  cmd.get("summary"), cmd.get("category"), cmd.get("relevance"))
        # find y esc no requieren acción de escritura

    history.add_message(conn, conv_id, 'assistant', answer)
    return answer
