import sqlite3
import json
from datetime import datetime
from termux_backend.modules.modulo_tools.utils import get_db_path

DB_PATH = get_db_path()

# ------------------------------
# Mapeo de módulo a criptomoneda
# ------------------------------
MODULE_CRYPTO = {
    "":        "NRN",       # módulo genérico
    "symcontext": "SYMCOIN",
    "bitacora":   "MOODBIT",
    "modulo_ai":  "AITHOUGHT",
    "clarai":     "CLARIUM",
    # 'SYNAP' para herramienta
}

NFT_CRYPTO = "neuroNFT"  # para mint_nft

def mint_token(module, action, amount=1, input_id=None, metadata={}):
    from datetime import datetime
    crypto = MODULE_CRYPTO.get(module, "SYNAP")
    ts     = datetime.now().isoformat()

    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO neuro_tokens
            (module, action, amount, input_id, metadata, timestamp, crypto)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        module,
        action,
        amount,
        input_id,
        json.dumps(metadata),
        ts,
        crypto
    ))
    conn.commit()
    conn.close()

    print(f"🪙 Token minado: {amount} · módulo={module} · acción={action} · crypto={crypto}")

def mint_nft(input_id, title=None, metadata={}):
    from datetime import datetime
    ts     = datetime.now().isoformat()
    crypto = NFT_CRYPTO

    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO neuro_nfts
            (input_id, title, metadata, timestamp, crypto)
        VALUES (?, ?, ?, ?, ?)
    """, (
        input_id,
        title,
        json.dumps(metadata),
        ts,
        crypto
    ))
    conn.commit()
    conn.close()

    print(f"🖼️ NFT creado  · input_id={input_id} · title='{title or ''}' · crypto={crypto}")


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
