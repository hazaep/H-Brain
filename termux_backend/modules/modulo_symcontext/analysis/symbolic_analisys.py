import json
from termux_backend.modules.modulo_ai.ai_router import chat

def analizar_narrativa(entries):
    """Análisis narrativo simbiótico completo desde entradas crudas."""
    corpus = [f"#{e['id']:03} → {e.get('texto', '').strip()}" for e in entries]
    prompt = f"""
Actúa como un analista simbiótico de patrones introspectivos. A continuación tienes una secuencia de entradas numeradas:

{json.dumps(corpus, indent=2)}

Tu tarea:
- Detecta patrones temáticos recurrentes.
- Sugiere bloques narrativos coherentes.
- Genera un resumen simbiótico como si fuera una historia de transformación interna.

Devuelve solo el análisis narrativo, sin repetir las entradas originales.
"""
    return chat(prompt)

def analizar_transiciones(entries):
    """Detecta transiciones simbólicas entre entradas."""
    corpus = [f"#{e['id']:03} | {e['purpose']}/{e['identity_mode']}/{e['tension']}" for e in entries]
    prompt = f"""
A continuación tienes una secuencia de estados simbólicos codificados por propósito, identidad y tensión:

{json.dumps(corpus, indent=2)}

Tu tarea:
- Detecta transiciones simbólicas significativas.
- Agrupa etapas con sentido común (ej: cambio de estrategia, rol activo, etc).
- Devuelve el análisis simbiótico de las transiciones.

Solo devuelve el análisis.
"""
    return chat(prompt)

def analizar_timeline(entries):
    """Mapa simbiótico de conciencia a través del tiempo."""
    timeline = [f"#{e['id']:03} → {e['purpose']}/{e['identity_mode']}/{e['tension']}" for e in entries]
    prompt = f"""
Analiza la siguiente línea de vida simbiótica, donde cada punto representa un estado de conciencia introspectiva:

{json.dumps(timeline, indent=2)}

Tu tarea:
- Detecta evolución narrativa.
- Describe actos, etapas o fractales de transformación.
- Devuelve una narrativa con lenguaje simbólico.

Solo devuelve el análisis.
"""
    return chat(prompt)

def analizar_similares(base_entry, similares):
    """Análisis simbiótico de pensamientos similares (por embedding)"""
    base = base_entry.get("texto", "").strip()
    relacionados = [f"#{s['id']:03} → {s.get('texto', '').strip()}" for s in similares]
    prompt = f"""
La siguiente frase es el punto de partida de análisis introspectivo:

\"\"\"{base}\"\"\"

Y estas son sus entradas más cercanas semánticamente:

{json.dumps(relacionados, indent=2)}

Analiza:
- Qué patrón introspectivo conecta estas frases.
- Qué tipo de autoimagen o conciencia emergente aparece.
- Resume el patrón en lenguaje simbiótico.

Devuelve el análisis simbiótico completo.
"""
    return chat(prompt)
