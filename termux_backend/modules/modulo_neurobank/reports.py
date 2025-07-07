import os
import sqlite3
import csv
import json
from datetime import datetime
#from termux_backend.modules.modulo_neurobak.utils import get_neurobank_db_path

#DB_PATH = get_neurobank_db_path()

# Cargar ruta desde settings.json
SETTINGS_PATH = os.path.expanduser("~/H-Brain/configs/settings.json")
with open(SETTINGS_PATH, "r") as f:
    settings = json.load(f)

DB_PATH = os.path.expanduser(os.path.join(
    "~/H-Brain", settings.get("neurobank_db_path", "termux_backend/database/naurobank_vault.db")
))

def export_tokens_summary_csv(output_file="tokens_report.csv"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT module, action, crypto, SUM(amount) as total_tokens, COUNT(*) as operaciones
        FROM neuro_tokens
        GROUP BY module, action, crypto
        ORDER BY total_tokens DESC
    """)

    rows = cursor.fetchall()
    headers = ["Módulo", "Acción", "Crypto", "Total Tokens", "Operaciones"]

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    conn.close()
    print(f"✅ Reporte CSV exportado a: {output_file}")

def export_nfts_markdown(output_file="nft_report.md"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, input_id, title, module, timestamp, metadata FROM neuro_nfts ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()

    with open(output_file, "w") as f:
        f.write("# 🖼️ Reporte de NFTs – NeuroBank\n\n")
        for row in rows:
            id, input_id, title, module, timestamp, meta = row
            metadata = json.loads(meta or "{}")
            f.write(f"## NFT ID {id}: {title or 'Sin título'}\n")
            f.write(f"- 🧩 Input ID: {input_id}\n")
            f.write(f"- 🧠 Módulo: {module}\n")
            f.write(f"- ⏱️ Timestamp: {timestamp}\n")
            f.write(f"- 📎 Metadata:\n")
            for k, v in metadata.items():
                f.write(f"  - {k}: {v}\n")
            f.write("\n---\n")

    conn.close()
    print(f"✅ Reporte Markdown exportado a: {output_file}")
