import os, json  
from openai import OpenAI  
from termux_backend.modules.modulo_clarai import history, memory, embedding_tools  
from termux_backend.modules.modulo_tools.utils import get_settings  
  
_cfg = get_settings()  
CLARAI_CFG = _cfg.get("clarai", {})  
MODEL = CLARAI_CFG.get("model", "deepseek-reasoner")  
API_URL = CLARAI_CFG.get("api_url", "https://api.deepseek.com")  
TEMP = CLARAI_CFG.get("temperature", 1.3)  
CATS = CLARAI_CFG.get("memory_categories", ["proyectos", "usuario", "aprendizaje"])  
MAX_TOK = CLARAI_CFG.get("max_tokens", 20000)  
KEY_PATH = os.path.expanduser(CLARAI_CFG.get("ai_key_path", "configs/secrets/deepseek_key.txt"))  
ESPECIALIZACION = CLARAI_CFG.get("especializacion", "Exploración y teoria")  
EMBED_MODEL = CLARAI_CFG.get("embedding_model", "text-embedding-3-small")  
N_USER_SIMILAR = CLARAI_CFG.get("n_user_similar", 4)  
N_ASSISTANT_SIMILAR = CLARAI_CFG.get("n_assistant_similar", 2)  
N_MEMORY_SIMILAR = CLARAI_CFG.get("n_memory_similar", 4)  
  
def get_api_key():  
    return open(os.path.expanduser(KEY_PATH)).read().strip()  
  
def build_system_prompt(username, memories, items, search_results=None, semantic_memories=None, semantic_msgs=None):  
    lines = []  
      
    # Memorias base por relevancia  
    for m in memories:  
        lines.append(f"- [{m[0]}] Mem: {m[1]} Cat: {m[2]} Relevancia: {m[3]}")  
      
    # Resultados por búsqueda explícita (find:)  
    if search_results:  
        for m in search_results:  
            lines.append(f"- [F:{m[0]}] Mem: {m[1]} Cat: {m[2]} Relevancia: {m[3]}")  
      
    # Resultados semánticos por embedding  
    if semantic_memories:  
        for m in semantic_memories:  
            lines.append(f"- [S:{m[0]}] Mem: {m[1]} Cat: {m[2]} Relevancia: {m[3]}")  
  
    # Similares por historial semántico  
    msg_lines = []  
    if semantic_msgs:  
        for msg in semantic_msgs:  
            if msg["role"] == "user":  
                msg_lines.append(f"> Usuario dijo (sim={msg['sim']:.2f}): {msg['content']}")  
            elif msg["role"] == "assistant":  
                msg_lines.append(f"> Clarai respondió (sim={msg['sim']:.2f}): {msg['content']}")  
# === Visualización CLI de contexto ===  
    print("\n\n_____[CLARIUM] CONTEXTO =====================")  
  
    if semantic_msgs:  
        print("\n🔍 Mensajes similares por embedding:")  
        for msg in semantic_msgs:  
            rol = "🤖 Clarai" if msg["role"] == "assistant" else "🧠 Usuario"  
            print(f"{rol} (sim={msg['sim']:.2f}): {msg['content']}")  
  
    if semantic_memories:  
        print("\n📦 Memorias similares por embedding:")  
        for mem in semantic_memories:  
            print(f"[S:{mem[0]}] Cat: {mem[2]} ({mem[3]}) → {mem[1]}")  
  
    if search_results:  
        print("\n🔎 Memorias encontradas por keyword (find:):")  
        for m in search_results:  
            print(f"[F:{m[0]}] Cat: {m[2]} ({m[3]}) → {m[1]}")  
  
    if memories:  
        print("\n📌 Memorias destacadas por relevancia:")  
        for m in memories:  
            print(f"[{m[0]}] Cat: {m[2]} ({m[3]}) → {m[1]}")  
  
    print("____________________________________________\n")  
  
    return f"""Eres Clarai, asistente de IA creada por Hazael. Usuario: {username}  
  
Especialización actual:  
1.- {ESPECIALIZACION}  
  
Reglas:  
- Ajustar estilo según historial  
- Gestionar el historial relevante según tu criterio (puedes incluir múltiples comandos por respuesta)  
  
## CONTEXTO SEMÁNTICO RELEVANTE:  
{chr(10).join(msg_lines)}  
  
## INSTRUCCIONES DE MEMORIA  
Evalúa cada interacción y decide si:  
- Agregar memoria nueva (add): ¿Es información útil a largo plazo?  
- Eliminar memoria (del): ¿Ha perdido relevancia?  
- Modificar (rew): ¿Requiere actualización?  
- Omitir (esc): ¿No es memorable?  
  
Criterios:  
1. Relevancia >7.0 para considerar almacenamiento (10.0 es crítico, 0.0 irrelevante)  
2. Categorías disponibles: {items}  
  
Comandos válidos (máximo 5, separados por coma [,]):  
- add: Mem: [resumen] Cat: [categoría] Relevancia: [X.X]  
- del: [id]  
- rew: [id] Mem: [...] Cat: [...] Relevancia: [X.X]  
- esc:  
  
🟡 IMPORTANTE: Siempre responde en formato JSON:  
{{  
  "respuesta": "texto de respuesta al usuario",  
  "comando": [ "comando1", "comando2", ... ]  
}}  
  
# Memoria actual:  
{chr(10).join(lines)}  
""".strip()  
# ... [encabezado sin cambios] ...

def send_message(username, conv_id, user_input):
    # Inicializar DBs
    conn = history.init_history_db()
    mem_conn = memory.init_memory_db()
    user_id = history.get_or_create_user(conn, username)

    # Guardar input del usuario
    msg_id_user = history.add_message(conn, conv_id, 'user', user_input)

    # Obtener embedding del input actual
    input_emb = embedding_tools.generate_embedding(user_input)

    # Guardar embedding del usuario
    try:
        embedding_tools.insert_message_embedding(conn, msg_id_user, "user", input_emb)
    except Exception as e:
        print(f"[!] Error guardando embedding de USER ID {msg_id_user}: {e}")

    # Buscar mensajes más similares por embedding
    sim_msgs = embedding_tools.search_similar_message_embeddings(conn, input_emb, top_n=N_USER_SIMILAR + N_ASSISTANT_SIMILAR)
    semantic_msgs = []
    for sim, msg_id, role in sim_msgs:
        if role not in ["user", "assistant"]:
            continue
        cur = conn.execute("SELECT content FROM messages WHERE id=? AND role=?", (msg_id, role))
        row = cur.fetchone()
        if row:
            semantic_msgs.append({"role": role, "content": row[0], "sim": sim})

    # Buscar memorias similares por embedding
    sim_mems_raw = embedding_tools.search_similar_memory_embeddings(mem_conn, input_emb, top_n=N_MEMORY_SIMILAR)
    semantic_mems = []
    for sim, mem_id in sim_mems_raw:
        row = memory.get_memory_by_id(mem_conn, mem_id)
        if row:
            semantic_mems.append((row[0], row[1], row[2], row[3]))  # id, summary, category, relevance

    # Búsqueda por palabra clave (find:)
    search = []
    if user_input.lower().startswith("find:"):
        kw = user_input.split(":", 1)[1].strip()
        search = memory.search_memories(mem_conn, user_id, kw)

    # Cargar memorias top y mensajes de la conversación
    top_mems = memory.load_top_memories(mem_conn, user_id)
    history_msgs = history.fetch_history(conn, conv_id)

    # Construir system prompt con memoria, contexto semántico, etc.
    system = build_system_prompt(username, top_mems, CATS, search_results=search, semantic_memories=semantic_mems, semantic_msgs=semantic_msgs)
    messages = [{"role": "system", "content": system}] + history_msgs

    # Enviar a la API
    client = OpenAI(
        api_key=f"{get_api_key()}",
        base_url=API_URL,
    )
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOK,
        response_format={'type': 'json_object'},
        temperature=TEMP
    )

    reasoning = resp.choices[0].message.reasoning_content
    content = resp.choices[0].message.content

    # Procesar respuesta JSON
    if isinstance(content, dict):
        data = content
    elif isinstance(content, str):
        content = content.strip()
        if not content.startswith("{"):
            msg_id_assistant = history.add_message(conn, conv_id, 'assistant', content)
            try:
                emb = embedding_tools.generate_embedding(content)
                embedding_tools.insert_message_embedding(conn, msg_id_assistant, "assistant", emb)
            except Exception as e:
                print(f"[!] Error guardando embedding de ASSISTANT ID {msg_id_assistant}: {e}")
            return content, "", reasoning
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
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
    if isinstance(raw_comandos, str):
        raw_comandos = [raw_comandos]

    # Ejecutar comandos de memoria
    for cmd_str in raw_comandos:
        cmd = memory.process_memory_command(cmd_str)
        if not cmd:
            continue
        action = cmd["action"]
        if action == "add":
            mem_id = memory.add_memory(mem_conn, user_id, cmd["summary"], cmd["category"], cmd["relevance"])
            try:
                emb = embedding_tools.generate_embedding(cmd["summary"])
                embedding_tools.insert_memory_embedding(mem_conn, mem_id, emb)
            except Exception as e:
                print(f"[!] Error generando embedding para memoria ID {mem_id}: {e}")
        elif action == "del":
            memory.delete_memory(mem_conn, user_id, cmd["id"])
        elif action == "rew":
            memory.rewrite_memory(mem_conn, user_id, cmd["id"], cmd.get("summary"), cmd.get("category"), cmd.get("relevance"))

    # Guardar respuesta del assistant
    msg_id_assistant = history.add_message(conn, conv_id, 'assistant', answer)

    # Generar y guardar embedding del assistant
    try:
        emb = embedding_tools.generate_embedding(answer)
        embedding_tools.insert_message_embedding(conn, msg_id_assistant, "assistant", emb)
    except Exception as e:
        print(f"[!] Error guardando embedding de ASSISTANT ID {msg_id_assistant}: {e}")

    return answer, raw_comandos, reasoning

