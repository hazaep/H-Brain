🚀 Instalación

Desde la raíz de H-Brain:
```
cd ~/H-Brain
# Instalar dependencias Python
pip install -r termux_backend/requirements.txt
# (Flask, openai-python, networkx, matplotlib, etc.)

```
Configura tu API Key editando:
```
# configs/settings.json
{
  "openai_key_path": "configs/secrets/openai_key.txt",
  "default_model": "gpt-3.5-turbo",
  "embedding_model": "text-embedding-3-small",
  ...
}
```
