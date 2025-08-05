import os, json, requests
from termux_backend.modules.modulo_clarai import history, memory
from termux_backend.utils.debug import log_debug
# Si decides usar el enrutador de modulo_ai:
# from termux_backend.modules.modulo_ai.ai_router import route_request

_cfg      = json.load(open(os.path.expanduser("~/H-Brain/configs/settings.json")))
API_URL   = _cfg["clarai_api_url"]
MODEL     = _cfg["clarai_model"]
TEMP      = _cfg["clarai_temperature"]
KEY_PATH  = _cfg["deepseek_key_path"]
CATS      = _cfg["clarai_memory_categories"]
MAX_TOK   = _cfg["clarai_max_tokens"]

def get_api_key():
    return open(os.path.expanduser(KEY_PATH)).read().strip()

def build_system_prompt(username, memories, items, search_results=None):
    lines = []
    for m in memories:
        lines.append(f"- [{m[0]}] Mem: {m[1]} Cat: {m[2]} Relevancia: {m[3]}")
    if search_results:
        for m in search_results:
            lines.append(f"- [F:{m[0]}] Mem: {m[1]} Cat: {m[2]} Relevancia: {m[3]}")
    print("\n\n_____[CLARIUM]_____________________________")
    for l in lines:
        print(l)
    print("\n___________________________________________")
    return f"""Eres Clarai, asistente de IA creada por Hazael. Usuario: {username}

Especialización actual:
1.- Exploración teórica

Reglas:
- Ajustar estilo según historial
- Gestionar el historial relevante según tu criterio (puedes incluir múltiples comandos por respuesta)

## INSTRUCCIONES DE MEMORIA
Evalúa cada interacción y decide si:
- Agregar memoria nueva (add): ¿Es información útil a largo plazo?
- Eliminar memoria (del): ¿Ha perdido relevancia?
- Modificar (rew): ¿Requiere actualización?
- Buscar (find): ¿Necesitas contexto histórico?
- Omitir (esc): ¿No es memorable?

Criterios:
1. Relevancia >7.0 para considerar almacenamiento (10.0 es crítico, 0.0 irrelevante)
2. Categorías disponibles: {items}

Comandos válidos (maximo 5, separados por coma [,]):
- add: Mem: [resumen] Cat: [categoría] Relevancia: [X.X]
- del: [id]
- rew: [id] Mem: [...] Cat: [...] Relevancia: [X.X]
- find: [palabras clave] # find out of service
- esc:

🟡 IMPORTANTE: Siempre responde en formato JSON:
{{
  "respuesta": "texto de respuesta al usuario",
  "comando": [ "comando1", "comando2", ... ]
}}

# Memoria actual:
{chr(10).join(lines)}
""".strip()

def send_message(username, conv_id, user_input):
    # Inicializar DBs
    conn = history.init_history_db()
    mem_conn = memory.init_memory_db()
    user_id = history.get_or_create_user(conn, username)

    # Guardar input del usuario
    history.add_message(conn, conv_id, 'user', user_input)

    # Cargar historial y memorias relevantes
    history_msgs = history.fetch_history(conn, conv_id)
    top = memory.load_top_memories(mem_conn, user_id)
    search = []
    if user_input.lower().startswith("find:"):
        kw = user_input.split(":",1)[1].strip()
        search = memory.search_memories(mem_conn, user_id, kw)

    # Preparar prompt
    system = build_system_prompt(username, top, CATS, search)
    messages = [{"role":"system","content":system}] + history_msgs
#    print(system)
    log_debug(system)
    # Enviar a la API (o router si usas uno)
    payload = {'model': MODEL, 'messages': messages, 'temperature': TEMP, 'max_tokens': MAX_TOK}
    headers = {'Authorization': f'Bearer {get_api_key()}', 'Content-Type': 'application/json'}
    resp = requests.post(API_URL, headers=headers, json=payload)

    if resp.status_code != 200:
        return f"[Error {resp.status_code}] {resp.text}"

    content = resp.json()['choices'][0]['message']['content']

    # Soportar simulación con dict o respuesta real como str
    if isinstance(content, dict):
        data = content
    elif isinstance(content, str):
        content = content.strip()
        if not content.startswith("{"):
            history.add_message(conn, conv_id, 'assistant', content)
            return content
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Intentar descomponer línea por línea si hay múltiples JSONs
            for line in content.strip().splitlines():
                try:
                    data = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue
            if not data:
                raise
    else:
        raise TypeError(f"Tipo inesperado en respuesta IA: {type(content)}")

    answer = data.get("respuesta", "")
    raw_comandos = data.get("comando", [])

    # Asegurar que raw_comandos sea lista
    if isinstance(raw_comandos, str):
        raw_comandos = [raw_comandos]

    log_debug("Respuesta IA JSON:\n" + json.dumps(data, indent=2))

    # Ejecutar cada comando individualmente
    for cmd_str in raw_comandos:
        cmd = memory.process_memory_command(cmd_str)
        if not cmd:
            continue
        action = cmd["action"]
        if action == "add":
            memory.add_memory(mem_conn, user_id, cmd["summary"], cmd["category"], cmd["relevance"])
        elif action == "del":
            memory.delete_memory(mem_conn, user_id, cmd["id"])
        elif action == "rew":
            memory.rewrite_memory(mem_conn, user_id, cmd["id"], cmd.get("summary"), cmd.get("category"), cmd.get("relevance"))
        # find y esc no requieren ejecución directa

    history.add_message(conn, conv_id, 'assistant', answer)
    return answer, raw_comandos
