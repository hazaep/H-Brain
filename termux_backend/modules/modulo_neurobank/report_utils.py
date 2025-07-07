import sqlite3
import csv
from datetime import datetime
from termux_backend.modules.modulo_tools.utils import get_settings

settings = get_settings()
DB_PATH = settings["neurobank_db_path"]

def export_tokens_summary_csv(output_path):
    """
    Genera un reporte CSV con el resumen de tokens minados por módulo y acción.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT module, action, COUNT(*), SUM(amount)
        FROM neuro_tokens
        GROUP BY module, action
    """)
    rows = cursor.fetchall()
    conn.close()

    with open(output_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Módulo", "Acción", "Cantidad de Registros", "Total Tokens"])
        writer.writerows(rows)
    
    print(f"📄 Reporte CSV generado en {output_path}")


def export_nfts_markdown(output_path):
    """
    Genera un reporte en formato Markdown con todos los NFTs registrados.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, input_id, title, crypto, timestamp, metadata FROM neuro_nfts")
    rows = cursor.fetchall()
    conn.close()

    with open(output_path, "w") as f:
        f.write(f"# 📦 Reporte NFT - {datetime.now().isoformat()}\n\n")
        for id_, input_id, title, crypto, timestamp, metadata in rows:
            f.write(f"## 🖼️ NFT ID: {id_} | {title or 'Sin título'}\n")
            f.write(f"- 🎯 input_id: {input_id}\n")
            f.write(f"- 💎 crypto: {crypto or 'No definida'}\n")
            f.write(f"- 🕒 timestamp: {timestamp or 'N/A'}\n")
            f.write(f"- 📎 metadata:\n```json\n{metadata}\n```\n\n")
    
    print(f"📝 Reporte Markdown generado en {output_path}")
