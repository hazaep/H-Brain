import os
import sqlite3
import json
import re

# Lee settings.json para rutas de memoria
def load_settings():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
    settings_path = os.path.join(project_root, "configs", "settings.json")
    with open(settings_path) as f:
        return json.load(f)

_cfg = load_settings()
MEMORY_DB = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")), _cfg.get("memory_db_path", "termux_backend/database/clarai_memory.db"))
MEMORY_CATEGORIES = _cfg.get("memory_categories", ["proyectos", "Clarai", "usuario", "aprendizaje"])
MAX_MEMORIES = _cfg.get("max_memories", 20)


def init_memory_db():
    conn = sqlite3.connect(MEMORY_DB)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                summary TEXT NOT NULL,
                category TEXT NOT NULL,
                relevance REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
    return conn


def load_top_memories(conn, user_id, limit=5):
    cur = conn.execute(
        "SELECT id, summary, category, relevance FROM memories WHERE user_id = ? ORDER BY relevance DESC LIMIT ?",
        (user_id, limit)
    )
    return cur.fetchall()


def add_memory(conn, user_id, summary, category, relevance):
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM memories WHERE user_id = ?", (user_id,))
        count = cur.fetchone()[0]
        if count < MAX_MEMORIES:
            conn.execute(
                "INSERT INTO memories (user_id, summary, category, relevance) VALUES (?, ?, ?, ?)",
                (user_id, summary, category, relevance)
            )
        else:
            conn.execute(
                "DELETE FROM memories WHERE id = (SELECT id FROM memories WHERE user_id = ? ORDER BY relevance ASC LIMIT 1)",
                (user_id,)
            )
            conn.execute(
                "INSERT INTO memories (user_id, summary, category, relevance) VALUES (?, ?, ?, ?)",
                (user_id, summary, category, relevance)
            )


def delete_memory(conn, user_id, mem_id):
    with conn:
        conn.execute(
            "DELETE FROM memories WHERE id = ? AND user_id = ?",
            (mem_id, user_id)
        )


def rewrite_memory(conn, user_id, mem_id, new_summary=None, new_cat=None, new_rel=None):
    with conn:
        if new_summary:
            conn.execute(
                "UPDATE memories SET summary = ? WHERE id = ? AND user_id = ?",
                (new_summary, mem_id, user_id)
            )
        if new_cat:
            conn.execute(
                "UPDATE memories SET category = ? WHERE id = ? AND user_id = ?",
                (new_cat, mem_id, user_id)
            )
        if new_rel is not None:
            conn.execute(
                "UPDATE memories SET relevance = ? WHERE id = ? AND user_id = ?",
                (new_rel, mem_id, user_id)
            )


def search_memories(conn, user_id, keyword, limit=5):
    pattern = f"%{keyword}%"
    cur = conn.execute(
        "SELECT id, summary, category, relevance FROM memories WHERE user_id = ? AND summary LIKE ? ORDER BY relevance DESC LIMIT ?",
        (user_id, pattern, limit)
    )
    return cur.fetchall()
