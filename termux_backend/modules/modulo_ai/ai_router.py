import json
from pathlib import Path

# Carga settings.json
SETTINGS_PATH = Path(__file__).resolve().parents[3] / "configs/settings.json"
try:
    with open(SETTINGS_PATH, "r") as f:
        settings = json.load(f)
except Exception as e:
    print(f"❌ Error al leer settings.json en ai_router.py: {e}")
    settings = {}

provider_preference = settings.get("providers_preference", [])
embedding_model = settings.get("embedding_model", "text-embedding-3-small")

# Importar todos los clientes disponibles (aquí solo uno por ahora)
#from openai_client import chat_openai, embed_openai
# al principio de ai_router.py
try:
    from openai_client import chat_openai, embed_openai
except ImportError:
    # fallback para ejecución como parte de paquete
    from .openai_client import chat_openai, embed_openai

# Router para llamadas de chat
def chat(prompt):
    for provider in provider_preference:
        if provider == "openai":
            return chat_openai(prompt)
        # aquí puedes agregar: elif provider == "deepseek": ...
    return {"error": "No hay proveedor válido configurado."}

# Router para embeddings
def embed(text):
    for provider in provider_preference:
        if provider == "openai":
            return embed_openai(text, model=embedding_model)
    return {"error": "No hay proveedor válido para embedding."}
