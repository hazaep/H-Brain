from termux_backend.modules.modulo_neurobank import init_neurobank_schema
from termux_backend.modules.modulo_neurobank.neurobank import mint_token, mint_nft, get_balance

# Inicializar tablas si no existen
init_neurobank_schema()

# Minar un token de prueba
mint_token(
    module="test_module",
    action="test_action",
    amount=3,
    metadata={"nota": "prueba inicial de token"}
)

# Crear NFT ficticio (usa ID arbitrario de entrada)
mint_nft(
    input_id=1,
    title="NFT de prueba",
    metadata={"contexto": "entrada demo para pruebas"}
)

# Ver balance actual
balance = get_balance()
print(f"💰 Balance total: {balance}")
