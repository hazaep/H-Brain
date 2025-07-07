import sqlite3
import json
from datetime import datetime
import os
import sys
import json
#from termux_backend.modules.modulo_neurobank.utils import get_neurobank_db_path
#DB_PATH = get_neurobank_db_path()

# Cargar ruta desde settings.json
SETTINGS_PATH = os.path.expanduser("~/H-Brain/configs/settings.json")
with open(SETTINGS_PATH, "r") as f:
    settings = json.load(f)

DB_PATH = os.path.expanduser(os.path.join(
    "~/H-Brain", settings.get("neurobank_db_path", "termux_backend/database/naurobank_vault.db")
))

# Criptos registradas en el sistema
REGISTERED_CRYPTOS = {
    "NRN": "Neuron – Token principal del sistema",
    "SYNAP": "Synaptium – Token por uso de herramientas",
    "SYMCOIN": "Symbolic Coin – Módulo SymContext",
    "MOODBIT": "MoodBit – Módulo Bitácora",
    "AITHOUGHT": "AI Thought Token – Módulo IA",
    "Clarium": "Clarium – Módulo Clarai",
    "neuroNFT": "NeuroGem – NFT de introspección"
}


def mint_token(module, action, amount=1, input_id=None, crypto="NRN", metadata={}):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    metadata_str = json.dumps(metadata)
    cursor.execute("""
        INSERT INTO neuro_tokens (module, action, amount, input_id, crypto, metadata, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (module, action, amount, input_id, crypto, f"{metadata_str}", datetime.now().isoformat()))

    conn.commit()
    conn.close()
    print(f"🪙 Token minado: {amount} x [{crypto}] | módulo: {module}, acción: {action}")

def mint_nft(input_id, title=None, crypto="neuroNFT", metadata={}, module="Neurobank"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    metadata_str = json.dumps(metadata)
    cursor.execute("""
        INSERT INTO neuro_nfts (input_id, title, crypto, metadata, timestamp, module)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (input_id, title, crypto, f"{metadata_str}", datetime.now().isoformat(), module))

    conn.commit()
    conn.close()
    print(f"🖼️ NFT creado para input {input_id} - {module} - {title or 'Sin título'}")

def get_balance(module=None, crypto=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT SUM(amount) FROM neuro_tokens"
    conditions = []
    values = []

    if module:
        conditions.append("module = ?")
        values.append(module)
    if crypto:
        conditions.append("crypto = ?")
        values.append(crypto)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, values)
    total = cursor.fetchone()[0] or 0
    conn.close()
    return total

def list_tokens(module=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if module:
        cursor.execute("""
            SELECT id, amount, module, action, crypto, metadata, timestamp
            FROM neuro_tokens
            WHERE module = ?
            ORDER BY id DESC
        """, (module,))
    else:
        cursor.execute("""
            SELECT id, amount, module, action, crypto, metadata, timestamp
            FROM neuro_tokens
            ORDER BY id DESC
        """)

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(f"🔹 ID: {row[0]} | {row[1]} x [{row[4]}] [{row[2]}::{row[3]}]")
        print(f"⏱️ {row[6]}")
        print(f"📎 {row[5]}\n")

def list_nfts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, input_id, title, crypto, metadata, timestamp, module
        FROM neuro_nfts
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(f"💠 NFT ID: {row[0]} | Título: {row[2]}")
        print(f"🔗 input_id: {row[1]}")
        print(f"⚙️ Modulo: {row[6]}")
        print(f"⏱️ {row[5]}")
        print(f"💎 [{row[3]}]")
        print(f"📎 {row[4]}\n")

def report_tokens_by_crypto():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT crypto, COUNT(*) as count, SUM(amount) as total_amount
        FROM neuro_tokens
        GROUP BY crypto
        ORDER BY total_amount DESC
    """)
    data = cursor.fetchall()
    conn.close()

    print("📈 Reporte por tipo de token:")
    for crypto, count, total in data:
        print(f"🔹 {crypto}: {count} transacciones, {total} tokens")

def report_tokens_by_module():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT module, COUNT(*) as count, SUM(amount) as total_amount
        FROM neuro_tokens
        GROUP BY module
        ORDER BY total_amount DESC
    """)
    data = cursor.fetchall()
    conn.close()

    print("🏗️ Reporte por módulo:")
    for module, count, total in data:
        print(f"🔸 {module}: {count} acciones, {total} tokens")

def report_nfts_by_module():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT module, COUNT(*) as nft_count
        FROM neuro_nfts
        GROUP BY module
    """)
    data = cursor.fetchall()
    conn.close()

    print("💎 Reporte de NFTs por módulo:")
    for module, nft_count in data:
        print(f"🧬 {module}: {nft_count} NFTs")

