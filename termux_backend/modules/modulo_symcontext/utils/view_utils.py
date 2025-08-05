import sqlite3
import os
from termux_backend.modules.modulo_tools.utils import get_settings

_cfg = get_settings()
SYM_CFG = _cfg.get("symcontext", {})
DB_PATH = os.path.expanduser(SYM_CFG.get("sym_db_path", "termux_backend/database/context.db"))

def obtener_todas_las_entradas(limit: int = None) -> list:
    """Devuelve todas las entradas ordenadas por timestamp ascendente. Puede limitar la cantidad."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = """
        SELECT id, input_text, purpose, identity_mode, tension, emotion, tags, timestamp
        FROM context_entries
        ORDER BY timestamp ASC
    """
    if limit:
        sql += f" LIMIT {limit}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    entradas = [
        {
            "id": row[0],
            "texto": row[1],
            "purpose": row[2],
            "identity_mode": row[3],
            "tension": row[4],
            "emotion": row[5],
            "tags": row[6],
            "timestamp": row[7]
        }
        for row in rows
    ]
    metadata_token(
        module="SymContext",
        action=f"Cargar entradas - Total: {len(entradas)}",
        funcion="termux_backend.modules.modulo_symcontext.utils.view_utils : obtener_todas_las_entradas",
        entrada=limit,
        salida=f"Se cargaron {len(entradas)} entradas",
        input_id="N/A",
        crypto="SYNAP"
    )
    return entradas
