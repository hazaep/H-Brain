import os, sqlite3, json, re
from termux_backend.utils.debug import log_debug

_cfg = json.load(open(os.path.expanduser("~/H-Brain/configs/settings.json")))
_MEM_DB = os.path.join(_cfg["base_dir"], _cfg["clarai_memory_db_path"])
CATS = _cfg["clarai_memory_categories"]  # ["proyectos","Clarai","usuario","aprendizaje"]
MAX = _cfg["clarai_max_memories"]  #20
EXT_SLT = _cfg["clarai_extra_slots"]  #5

def init_memory_db():
    conn = sqlite3.connect(_MEM_DB)
    with conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS memories (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL,
          summary TEXT NOT NULL,
          category TEXT NOT NULL,
          relevance REAL NOT NULL,
          timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    return conn

def load_top_memories(conn, user_id, limit=MAX):
    cur = conn.execute(
      "SELECT id,summary,category,relevance FROM memories WHERE user_id=? ORDER BY relevance DESC LIMIT ?",
      (user_id, limit)
    )
    return cur.fetchall()

def add_memory(conn, user_id, summary, category, relevance):
    with conn:
        cnt = conn.execute("SELECT COUNT(*) FROM memories WHERE user_id=?", (user_id,)).fetchone()[0]
        if cnt < MAX:
            conn.execute(
              "INSERT INTO memories(user_id,summary,category,relevance) VALUES(?,?,?,?)",
              (user_id, summary, category, relevance)
            )
        else:
            conn.execute("""
            DELETE FROM memories
             WHERE id=(SELECT id FROM memories WHERE user_id=? ORDER BY relevance ASC LIMIT 1)
            """, (user_id,))
            conn.execute(
              "INSERT INTO memories(user_id,summary,category,relevance) VALUES(?,?,?,?)",
              (user_id, summary, category, relevance)
            )

def delete_memory(conn, user_id, mem_id):
    with conn:
        conn.execute("DELETE FROM memories WHERE id=? AND user_id=?", (mem_id, user_id))

def rewrite_memory(conn, user_id, mem_id, new_summary=None, new_cat=None, new_rel=None):
    with conn:
        if new_summary:
            conn.execute(
              "UPDATE memories SET summary=? WHERE id=? AND user_id=?",
              (new_summary, mem_id, user_id)
            )
        if new_cat:
            conn.execute(
              "UPDATE memories SET category=? WHERE id=? AND user_id=?",
              (new_cat, mem_id, user_id)
            )
        if new_rel is not None:
            conn.execute(
              "UPDATE memories SET relevance=? WHERE id=? AND user_id=?",
              (new_rel, mem_id, user_id)
            )

def get_memory_by_id(conn, mem_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id, summary, category, relevance FROM memories WHERE id = ?", (mem_id,))
    return cursor.fetchone()

def search_memories(conn, user_id, keyword, limit=EXT_SLT):
    pat = f"%{keyword}%"
    cur = conn.execute("""
      SELECT id,summary,category,relevance
       FROM memories
       WHERE user_id=? AND summary LIKE ?
       ORDER BY relevance DESC LIMIT ?
    """, (user_id, pat, limit))
    return cur.fetchall()

def process_memory_command(cmd_str):
    """Parsea add:/del:/rew:/find:/esc:"""
    log_debug(f"Recibido para parsear: {cmd_str}")
    cmd_str = cmd_str.strip()
    try:
        if cmd_str.startswith("add:"):
            parts = cmd_str.split(":",1)[1].split(" Cat:")
            summ = parts[0].replace("Mem:","").strip()
            cat,rel = parts[1].split(" Relevancia:")
            return {"action":"add","summary":summ,"category":cat.strip(),"relevance":float(rel)}
        if cmd_str.startswith("del:"):
            return {"action":"del","id":int(cmd_str.split(":",1)[1])}
        if cmd_str.startswith("rew:"):
            mid = int(re.search(r"rew:\s*(\d+)",cmd_str).group(1))
            summ = re.search(r"Mem:\s*(.*?)\s+Cat:", cmd_str)
      #      summ = re.search(r"Mem:\s*([^C]+)",cmd_str)
            cat  = re.search(r"Cat:\s*(\w+)",cmd_str)
            rel  = re.search(r"Relevancia:\s*([\d\.]+)",cmd_str)
            return {
              "action":"rew","id":mid,
              "summary":summ.group(1).strip() if summ else None,
              "category":cat.group(1) if cat else None,
              "relevance":float(rel.group(1)) if rel else None
            }
        if cmd_str.startswith("find:"):
            return {"action":"find","keyword":cmd_str.split(":",1)[1].strip()}
        if cmd_str.startswith("esc:"):
            return {"action":"esc"}
    except:
        return None
    return None
