from fastapi import FastAPI, Request, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional
import unicodedata
from termux_backend.modules.modulo_tools.utils import get_settings
# Utils y configuración
from termux_backend.modules.modulo_symcontext.utils.input import save_input
from termux_backend.modules.modulo_symcontext.utils.semantic_search import buscar_similares_emb
from termux_backend.modules.modulo_symcontext.api.core_symctx import obtener_todas_las_entradas
from termux_backend.modules.modulo_symcontext.analysis.symbolic_analysis import (
    analizar_narrativa,
    analizar_transiciones,
    analizar_similares,
    analizar_timeline
)
# Configuración global y token
settings = get_settings()
SYM_CFG = settings.get("symcontext", {})
API_TOKEN = SYM_CFG.get("api_token", "")
# App FastAPI
app = FastAPI(title="SymContext API")

# 🔐 Autenticación por Token

def verificar_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Token inválido o no provisto")

# normalizar texto

def normalizar(texto):
    return unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode("utf-8")

#  📦 Esquemas de entrada 

class RegistroInput(BaseModel):
    texto: str

class TextoEntrada(BaseModel):
    texto: str

@app.post("/symctx/register")
def registrar_entrada(data: RegistroInput, _: str = Depends(verificar_token)):
    info = save_input(texto=data.texto)
    return {"status": "ok", "registrado": info}

@app.get("/symctx/view")
def ver_entradas(limit: int = Query(default=50, ge=1, le=500), _: str = Depends(verificar_token)):
    """
    Devuelve entradas introspectivas en orden temporal ascendente.
    Puedes limitar el número de resultados (default: 50, máximo: 500)
    """
    entradas = obtener_todas_las_entradas(limit=limit)
    return {"total": len(entradas), "entradas": entradas}

@app.post("/symctx/narrative")
def narrativa_ia(limit: int = Query(default=40, ge=1, le=200), _: str = Depends(verificar_token)):
    from termux_backend.modules.modulo_symcontext.api.core_symctx import obtener_todas_las_entradas
    entries = obtener_todas_las_entradas(limit=limit)
    if not entries:
        return {"error": "No hay entradas registradas"}
    analisis = analizar_narrativa(entries)
    return {"analisis": analisis, "usadas": len(entries)}

@app.post("/symctx/transitions")
def transiciones_ia(limit: int = Query(default=60, ge=1, le=200), _: str = Depends(verificar_token)):
    from termux_backend.modules.modulo_symcontext.api.core_symctx import obtener_todas_las_entradas
    entries = obtener_todas_las_entradas(limit=limit)
    if not entries:
        return {"error": "No hay entradas registradas"}
    analisis = analizar_transiciones(entries)
    return {"analisis": analisis, "usadas": len(entries)}

@app.post("/symctx/find_related")
def simbolicos_relacionados(data: TextoEntrada, top_n: int = Query(default=6, ge=1, le=20), _: str = Depends(verificar_token)):
    entradas = obtener_todas_las_entradas()

    normalizado_input = normalizar(data.texto)
    base = next((e for e in reversed(entradas) if normalizado_input in normalizar(e["texto"])), None)

    if not base:
        # No se encontró entrada base exacta, se usará el texto proporcionado como base temporal
        base = {"id": None, "texto": data.texto}

    similares, _ = buscar_similares_emb(data.texto, top_n=top_n)
    analisis = analizar_similares(base, [{"id": s[1], "texto": s[2]} for s in similares])

    return {
        "analisis": analisis,
        "similares_encontrados": len(similares),
        "base_id": base["id"] if base.get("id") else "no registrada"
    }

@app.post("/symctx/timeline")
def transiciones_ia(limit: int = Query(default=60, ge=1, le=200), _: str = Depends(verificar_token)):
    from termux_backend.modules.modulo_symcontext.api.core_symctx import obtener_todas_las_entradas
    entries = obtener_todas_las_entradas(limit=limit)
    if not entries:
        return {"error": "No hay entradas registradas"}
    analisis = analizar_timeline(entries)
    return {"analisis": analisis, "usadas": len(entries)}

@app.post("/symctx/similares")
def buscar_similares(data: TextoEntrada, _: str = Depends(verificar_token)):
    similares, _ = buscar_similares_emb(data.texto)
    return {"similares": [{"id": s[1], "texto": s[2], "distancia": s[0]} for s in similares]}

@app.get("/symctx/config")
def ver_config(_: str = Depends(verificar_token)):
    return SYM_CFG

# === SERVIDOR DE FRONTEND WEB SYMCONTEXT ===

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Ruta base del frontend (ajustada a tu estructura)
# ~/H-Brain/termux_backend/frontend/symctx/
frontend_dir = Path(__file__).resolve().parents[3] / "frontend" / "symctx"

# Servir archivos estáticos
app.mount("/symctx/css", StaticFiles(directory=frontend_dir / "css"), name="css")
app.mount("/symctx/js", StaticFiles(directory=frontend_dir / "js"), name="js")

# Motor de plantillas
templates = Jinja2Templates(directory=str(frontend_dir / "views"))

# Vistas HTML
@app.get("/symweb", response_class=HTMLResponse)
def vista_inicio(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/symweb/registrar", response_class=HTMLResponse)
def vista_registrar(request: Request):
    return templates.TemplateResponse("registrar.html", {"request": request})

@app.get("/symweb/view", response_class=HTMLResponse)
def vista_ver_entradas(request: Request):
    return templates.TemplateResponse("ver_entradas.html", {"request": request})

@app.get("/symweb/narrative", response_class=HTMLResponse)
def vista_narrativa(request: Request):
    return templates.TemplateResponse("narrativa.html", {"request": request})

@app.get("/symweb/transitions", response_class=HTMLResponse)
def vista_transiciones(request: Request):
    return templates.TemplateResponse("transiciones.html", {"request": request})

@app.get("/symweb/find_related", response_class=HTMLResponse)
def vista_find_related(request: Request):
    return templates.TemplateResponse("find_related.html", {"request": request})

@app.get("/symweb/timeline", response_class=HTMLResponse)
def vista_timeline(request: Request):
    return templates.TemplateResponse("timeline.html", {"request": request})
