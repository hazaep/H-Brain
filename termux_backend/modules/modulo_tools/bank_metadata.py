from datetime import datetime
from termux_backend.modules.modulo_neurobank.neurobank import mint_token, mint_nft

def metadata_token(module, action, funcion, entrada=None, salida=None, input_id=None, crypto="SYNAP"):
    origen = f"Modulo: {module} - Funcion: {funcion}"
    amount = 1
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "crypto": crypto,
        "origin": origen,
        "id": input_id,
        "data_input": entrada,
        "data_output": salida
    }
    mint_token(module, action, amount, input_id, crypto, metadata)

def metadata_nft(module, input_id, funcion, entrada=None, salida=None, title=None, crypto="neuroNFT"):
    origen = f"Modulo: {module} - Funcion: {funcion}"
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "crypto": crypto,
        "title": title,
        "origin": origen,
        "id": input_id,
        "data_input": entrada,
        "data_output": salida
    }

    mint_nft(input_id, title, crypto, metadata, module)

