#!/data/data/com.termux/files/usr/bin/bash

# Activar entorno virtual si es necesario
source ~/H-Brain/venv/bin/activate

# Ir a la carpeta base del proyecto
cd ~/H-Brain

# Iniciar servidor Uvicorn escuchando en toda la red
echo "🌐 Iniciando SymContext API accesible desde tu red local..."
echo "📡 Dirección de acceso: http://$(ip route get 1 | awk '{print $7; exit}'):8000/docs"
uvicorn termux_backend.modules.modulo_symcontext.api_symctx:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
