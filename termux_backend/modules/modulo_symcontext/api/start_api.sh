#!/data/data/com.termux/files/usr/bin/bash
# Script para iniciar la API de SymContext

cd /data/data/com.termux/files/home/H-Brain/
echo "🚀 Iniciando API SymContext en http://127.0.0.1:8000/docs"
PYTHONPATH=. uvicorn termux_backend.modules.modulo_symcontext.api.api_symctx:app --reload
