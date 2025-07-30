from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

# Utils y configuración
from termux_backend.modules.modulo_tools.utils import get_settings
from termux_backend.modules.modulo_symcontext.utils.input import save_input
from termux_backend.modules.modulo_symcontext.utils.semantic_search import buscar_similares_emb
from termux_backend.modules.modulo_symcontext.api.core_symctx import obtener_todas_las_entradas
from termux_backend.modules.modulo_symcontext.analysis.symbolic_analysis import (
    analizar_narrativa,
    analizar_transiciones,
    analizar_similares
)

# Configuración global y token
settings = get_settings()
SYM_CFG = settings.get("symcontext", {})
API_TOKEN = SYM_CFG.get("api_token", "")

# App FastAPI
app = FastAPI(title="SymContext API")

# ----------------------------- 🔐 Autenticación por Token -----------------------------

def verificar_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Token inválido o no provisto")

# ----------------------------- 📦 Esquemas de entrada -----------------------------

class RegistroInput(BaseModel):
    texto: str

class TextoEntrada(BaseModel):
    texto: str
    top_n: Optional[int] = 5  # valor por defecto

# ----------------------------- 📌 Endpoints protegidos -----------------------------

@app.post("/symctx/register")
def registrar_entrada(data: RegistroInput, _: str = Depends(verificar_token)):
    info = save_input(texto=data.texto)
    return {"status": "ok", "registrado": info}

@app.post("/symctx/similares")
def buscar_similares(data: TextoEntrada, _: str = Depends(verificar_token)):
    similares, _ = buscar_similares_emb(data.texto, top_n=data.top_n)
    return {"similares": [{"id": s[1], "texto": s[2], "distancia": s[0]} for s in similares]}

@app.post("/symctx/narrative")
def narrativa_ia(_: str = Depends(verificar_token)):
    entries = obtener_todas_las_entradas()
    if not entries:
        return {"error": "No hay entradas registradas"}
    analisis = analizar_narrativa(entries)
    return {"analisis": analisis}

@app.post("/symctx/transitions")
def transiciones_ia(_: str = Depends(verificar_token)):
    entries = obtener_todas_las_entradas()
    if not entries:
        return {"error": "No hay entradas registradas"}
    analisis = analizar_transiciones(entries)
    return {"analisis": analisis}

@app.post("/symctx/find_related")
def simbolicos_relacionados(data: TextoEntrada, _: str = Depends(verificar_token)):
    base = obtener_todas_las_entradas(data.texto)
    if not base:
        return {"error": "No se encontró entrada base"}
    similares, _ = buscar_similares_emb(data.texto, top_n=data.top_n)
    analisis = analizar_similares(base, [{"id": s[1], "texto": s[2]} for s in similares])
    return {
        "base_id": base["id"],
        "analisis": analisis,
        "similares_ids": [s[1] for s in similares]
    }

@app.get("/symctx/view")
def obtener_entradas(_: str = Depends(verificar_token)):
    entradas = obtener_todas_las_entradas()
    return {"entradas": entradas}

@app.get("/symctx/config")
def ver_config(_: str = Depends(verificar_token)):
    return SYM_CFG
