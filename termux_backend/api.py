from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from termux_backend.modules.modulo_symcontext.api.api_symctx import app as symctx_app

# Crear app principal
app = FastAPI(title="H-Brain API")

# Middleware CORS (para frontend web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir esto luego
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar la API de SymContext en /symctx/
app.mount("/", symctx_app)

# Ruta base informativa
@app.get("/")
def root():
    return {
        "mensaje": "🚀 API central de H-Brain en ejecución",
        "modulos_activos": ["/symctx"]
    }
