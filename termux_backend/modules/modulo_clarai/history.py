import os, sqlite3, json
from termux_backend.modules.modulo_tools.utils import get_settings

# Cargar configuración
_cfg = get_settings()
CLARAI_CFG = _cfg.get("clarai", {})
_HIST_DB = os.path.expanduser(CLARAI_CFG.get("history_db_path", "termux_backend/database/ai_history.db"))

def init_history_db():
    conn = sqlite3.connect(_HIST_DB)
    with conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS conversations (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL,
          name TEXT NOT NULL,
          started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS messages (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          conv_id INTEGER NOT NULL,
          role TEXT NOT NULL,
          content TEXT NOT NULL,
          timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(conv_id) REFERENCES conversations(id)
        );
        """)
    return conn

def get_or_create_user(conn, username):
    with conn:
        cur = conn.execute("SELECT id FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        if row: return row[0]
        cur = conn.execute("INSERT INTO users(username) VALUES(?)", (username,))
        return cur.lastrowid

def fetch_history(conn, conv_id, pairs=4):
    """Últimos `pairs` pares user/assistant = 2*pairs mensajes."""
    cur = conn.execute(
      "SELECT role,content FROM messages WHERE conv_id=? ORDER BY id DESC LIMIT ?",
      (conv_id, pairs*2)
    )
    rows = cur.fetchall()[::-1]  # invertir al orden cronológico  
    return [{"role": r, "content": c} for r,c in rows]

def add_message(conn, conv_id, role, content):
    with conn:
        conn.execute(
          "INSERT INTO messages(conv_id,role,content) VALUES(?,?,?)",
          (conv_id, role, content)
        )

