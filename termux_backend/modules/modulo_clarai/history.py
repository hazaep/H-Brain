import os
import sqlite3
import json

def load_settings():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
    settings_path = os.path.join(project_root, "configs", "settings.json")
    with open(settings_path) as f:
        return json.load(f)

# Carga rutas desde settings.json
_cfg = load_settings()
HISTORY_DB = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")), _cfg.get("history_db_path", "termux_backend/database/ai_history.db"))


def init_history_db():
    conn = sqlite3.connect(HISTORY_DB)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conv_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(conv_id) REFERENCES conversations(id)
            )""")
    return conn


def get_or_create_user(conn, username):
    with conn:
        cur = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur = conn.execute("INSERT INTO users (username) VALUES (?)", (username,))
        return cur.lastrowid


def fetch_history(conn, conv_id):
    cur = conn.execute(
        "SELECT role, content FROM messages WHERE conv_id = ? ORDER BY id",
        (conv_id,)
    )
    return [{"role": r, "content": c} for r, c in cur.fetchall()]


def add_message(conn, conv_id, role, content):
    with conn:
        conn.execute(
            "INSERT INTO messages (conv_id, role, content) VALUES (?, ?, ?)",
            (conv_id, role, content)
        )
