import os
import json
from pathlib import Path
from openai import OpenAI, OpenAIError

# Cargar configuración
SETTINGS_PATH = Path(__file__).resolve().parents[3] / "configs/settings.json"
try:
    with open(SETTINGS_PATH, "r") as f:
        settings = json.load(f)
except Exception as e:
    print(f"❌ No se pudo cargar settings.json en openai_client: {e}")
    settings = {}

# Obtener clave desde archivo
key_path = settings.get("openai_key_path")
if key_path:
    key_file = Path(__file__).resolve().parents[3] / key_path
    try:
        with open(key_file, "r") as f:
            api_key = f.read().strip()
            os.environ["OPENAI_API_KEY"] = api_key
            client = OpenAI()
    except Exception as e:
        print(f"❌ Error al leer API Key OpenAI: {e}")
        client = None
else:
    print("⚠️ No se especificó openai_key_path en settings.json")
    client = None

# Función de chat
def chat_openai(prompt):
    if not client:
        return {"error": "Cliente OpenAI no inicializado."}

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        return {"error": str(e)}

# Función de embedding
def embed_openai(text, model="text-embedding-3-small"):
    if not client:
        return {"error": "Cliente OpenAI no inicializado."}

    try:
        response = client.embeddings.create(
            input=[text],
            model=model
        )
        return response.data[0].embedding
    except OpenAIError as e:
        return {"error": str(e)}

