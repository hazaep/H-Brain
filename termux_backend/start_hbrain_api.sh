#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/H-Brain/
echo "🚀 Iniciando API H-Brain en http://127.0.0.0:8000/docs"
PYTHONPATH=. uvicorn termux_backend.api:app --host 0.0.0.0 --port 8000 --reload

