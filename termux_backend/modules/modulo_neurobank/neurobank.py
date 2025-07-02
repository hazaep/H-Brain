import sqlite3
import json
from datetime import datetime
from termux_backend.modules.modulo_tools.utils import get_db_path

DB_PATH = get_db_path()


def mint_token(module, action, amount=1, input_id=None, metadata={}):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO neuro_tokens (module, action, amount, input_id, metadata, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        module,
        action,
        amount,
        input_id,
        json.dumps(metadata),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    print(f"🪙 Token minado: {amount} | módulo: {module}, acción: {action}")


def mint_nft(input_id, title=None, metadata={}):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO neuro_nfts (input_id, title, metadata, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        input_id,
        title,
        json.dumps(metadata),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    print(f"🖼️ NFT creado para input #{input_id} - {title or 'Sin título'}")


def get_balance(module=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if module:
        cursor.execute("SELECT SUM(amount) FROM neuro_tokens WHERE module = ?", (module,))
    else:
        cursor.execute("SELECT SUM(amount) FROM neuro_tokens")
    total = cursor.fetchone()[0] or 0
    conn.close()
    print(f"📊 Balance total{' del módulo ' + module if module else ''}: {total}")
    return total


def list_tokens(module=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if module:
        cursor.execute("""
            SELECT id, module, action, amount, input_id, timestamp, metadata
            FROM neuro_tokens WHERE module = ? ORDER BY timestamp DESC
        """, (module,))
    else:
        cursor.execute("""
            SELECT id, module, action, amount, input_id, timestamp, metadata
            FROM neuro_tokens ORDER BY timestamp DESC
        """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("📭 No se encontraron tokens.")
        return

    for row in rows:
        id_, module, action, amount, input_id, timestamp, metadata = row
        print(f"🔹 ID: {id_} | {amount} x [{module}::{action}]")
        if input_id:
            print(f"🔗 input_id: {input_id}")
        print(f"⏱️ {timestamp}")
        print(f"📎 {metadata}\n")


def list_nfts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, input_id, title, timestamp, metadata
        FROM neuro_nfts ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("💨 No hay NFTs registrados.")
        return

    for row in rows:
        id_, input_id, title, timestamp, metadata = row
        print(f"💠 NFT ID: {id_} | Título: {title}")
        print(f"🔗 input_id: {input_id}")
        print(f"⏱️ {timestamp}")
        print(f"📎 {metadata}\n")
