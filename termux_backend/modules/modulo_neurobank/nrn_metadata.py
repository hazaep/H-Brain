import os
import json
import sqlite3
from datetime import datetime
from termux_backend.modules.modulo_tools.utils import get_settings
# Cargar configuración global y del módulo
_cfg = get_settings()
NB_CFG = _cfg.get("neurobank", {})

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
                metadata=metadata_para_token,
                crypto="NRN"
            )
            print(f"🧠 NRN minado correctamente. Metadata registrada.")
        except Exception as e:
            print(f"❌ Error al minar NRN: {e}")

