import os
import sys
import json
import sqlite3
from datetime import datetime
from termux_backend.modules.modulo_tools.utils import get_settings

# Cargar configuración del módulo NeuroBank
_cfg = get_settings()
NB_CFG = _cfg.get("neurobank", {})
SYNAP_TRACING = NB_CFG.get("enable_synap_tracing", False)
db_path = os.path.expanduser(NB_CFG.get("nb_db_path", "termux_backend/database/neurobank_vault.db"))
RESET_MAX = NB_CFG.get("reset_nrn", 500000)
METADATA_PATH = os.path.expanduser(NB_CFG.get("nrn_metadata", "termux_backend/database/nrn_metadata.json"))


def nrn_metadata(incremento, crypto, module=None):
    """
    Controla el costo acumulado y genera un token NRN cuando se supera el umbral configurado.
    
    Args:
        incremento (int): Costo que se suma por la acción.
        crypto (str): Tipo de token generado (SYMCOIN, AITHOUGHT, etc.)
        module (str): Módulo que generó el token. Si no se especifica, se clasifica como no_reclamado.
    """
    path = METADATA_PATH

    # Intentar cargar o inicializar la estructura
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Archivo corrupto. Reiniciando metadata.")
            data = {}
    else:
        data = {}

    # Inicialización base
    data.setdefault("costo", 0)
    data.setdefault("ultimo_balance", 0)
    data.setdefault("no_reclamados", {})

    category = module if module else "no_reclamados"
    data.setdefault(category, {})
    data[category].setdefault(crypto, 0)

    # Aplicar incremento
    data[category][crypto] += 1
    data["costo"] += incremento
    current_costo = data["costo"]

    # Condición de minado
    should_mint = RESET_MAX is not None and current_costo >= RESET_MAX
    metadata_para_token = None

    if should_mint:
        metadata_para_token = json.loads(json.dumps(data))  # Hacer copia profunda sin referencias
        metadata_para_token["Neuron"] = "Token principal de H-Brain"

        # Actualiza el balance acumulado y reinicia el costo
        data["ultimo_balance"] += data["costo"]
        data["costo"] = 0

    # Guardar el estado actualizado
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

    # Si corresponde, minar un nuevo Neuron
    if metadata_para_token:
        try:
            mint_token_nrn(
                module="neurobank",
                action=f"Minado automático de NRN al alcanzar {RESET_MAX} unidades",
                amount=1,
                input_id=datetime.now().strftime('%d%m%Y_%H%M%S'),
                metadata=str(metadata_para_token),
                crypto="NRN"
            )
            print(f"🧠 NRN minado correctamente. Metadata registrada.")
        except Exception as e:
            print(f"❌ Error al minar NRN: {e}")

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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    metadata_str = json.dumps(metadata)
    cursor.execute("""
        INSERT INTO neuro_tokens (module, action, amount, input_id, crypto, metadata, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (module, action, amount, input_id, crypto, f"{metadata_str}", datetime.now().isoformat()))

    conn.commit()
    conn.close()

    if crypto == "SYNAP":
        nrn_metadata(incremento=1, crypto=crypto, module=module)
        if SYNAP_TRACING:
            print(f"🧩 [SYNAP] Token minado: {amount} | módulo: {module}, acción: {action}")
    else:
        nrn_metadata(incremento=10, crypto=crypto, module=module)
        print(f"🪙 Token minado: {amount} | módulo: {module}, acción: {action}, crypto: {crypto}")

def mint_token_nrn(module, action, amount=1, input_id=None, crypto="NRN", metadata={}):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    metadata_str = json.dumps(metadata)
    cursor.execute("""
        INSERT INTO neuro_tokens (module, action, amount, input_id, crypto, metadata, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (module, action, amount, input_id, crypto, f"{metadata_str}", datetime.now().isoformat()))

    conn.commit()
    conn.close()
    print(f"🪙 Token minado: {amount} x [{crypto} 🧠]\n| módulo: {module}\n| acción: {action}\n| metadata:\n{metadata_str}")

def mint_nft(input_id, title=None, crypto="neuroNFT", metadata={}, module="Neurobank"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    metadata_str = json.dumps(metadata)
    cursor.execute("""
        INSERT INTO neuro_nfts (input_id, title, crypto, metadata, timestamp, module)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (input_id, title, crypto, f"{metadata_str}", datetime.now().isoformat(), module))

    conn.commit()
    conn.close()
    nrn_metadata(incremento=1000, crypto=crypto, module=module)
    print(f"🖼️ NFT creado para input {input_id} - {module} - {title or 'Sin título'}")

def get_balance(module=None, crypto=None):
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
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

