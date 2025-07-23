from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from termux_backend.modules.modulo_symcontext.utils.input import save_input
from termux_backend.modules.modulo_symcontext.utils.semantic_search import buscar_similares_emb
from termux_backend.modules.modulo_symcontext.api.core_symctx import obtener_todas_las_entradas
from termux_backend.modules.modulo_symcontext.analysis.symbolic_analysis import (
    analizar_narrativa,
    analizar_transiciones,
    analizar_similares
)

app = FastAPI(title="SymContext API")

class RegistroInput(BaseModel):
    texto: str
    purpose: Optional[str] = "otro"
    identity_mode: Optional[str] = "otro"
    tension: Optional[str] = "ninguna"
    emotion: Optional[str] = "neutral"
    tags: Optional[str] = ""

class TextoEntrada(BaseModel):
    texto: str

@app.post("/symctx/register")
def registrar_entrada(data: RegistroInput):
    info = save_input(
        texto=data.texto,
            #purpose=data.purpose,
            #identity_mode=data.identity_mode,
            #tension=data.tension,
            #emotion=data.emotion,
            #tags=data.tags
    )
    return {"status": "ok", "registrado": info}

@app.get("/symctx/view")
def ver_entradas(limit: int = Query(default=50, ge=1, le=500)):
    """
    Devuelve entradas introspectivas en orden temporal ascendente.
    Puedes limitar el número de resultados (default: 50, máximo: 500)
    """
    entradas = obtener_todas_las_entradas(limit=limit)
    return {"total": len(entradas), "entradas": entradas}

from fastapi import Query

@app.post("/symctx/narrative")
def narrativa_ia(limit: int = Query(default=40, ge=1, le=200)):
    from termux_backend.modules.modulo_symcontext.api.core_symctx import obtener_todas_las_entradas
    entries = obtener_todas_las_entradas(limit=limit)
    if not entries:
        return {"error": "No hay entradas registradas"}
    analisis = analizar_narrativa(entries)
    return {"analisis": analisis, "usadas": len(entries)}

@app.post("/symctx/transitions")
def transiciones_ia(limit: int = Query(default=60, ge=1, le=200)):
    from termux_backend.modules.modulo_symcontext.api.core_symctx import obtener_todas_las_entradas
    entries = obtener_todas_las_entradas(limit=limit)
    if not entries:
        return {"error": "No hay entradas registradas"}
    analisis = analizar_transiciones(entries)
    return {"analisis": analisis, "usadas": len(entries)}

@app.post("/symctx/find_related")
def simbolicos_relacionados(data: TextoEntrada):
    from termux_backend.modules.modulo_symcontext.api.core_symctx import obtener_todas_las_entradas
    entradas = obtener_todas_las_entradas()
    
    # Buscar entrada base que contenga el texto (última coincidencia)
    base = next((e for e in reversed(entradas) if data.texto.lower() in e['texto'].lower()), None)
    if not base:
        return {"error": "No se encontró entrada base con ese texto"}
    
    similares, _ = buscar_similares_emb(data.texto)
    analisis = analizar_similares(base, [{"id": s[1], "texto": s[2]} for s in similares])
    return {
        "base_id": base["id"],
        "analisis": analisis,
        "similares_encontrados": len(similares)
    }

@app.post("/symctx/similares")
def buscar_similares(data: TextoEntrada):
    similares, _ = buscar_similares_emb(data.texto)
    return {"similares": [{"id": s[1], "texto": s[2], "distancia": s[0]} for s in similares]}

