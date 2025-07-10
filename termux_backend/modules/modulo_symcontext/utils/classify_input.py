import os
import json
from termux_backend.modules.modulo_ai.ai_router import chat

def clasificar_input(user_input):
    prompt_base = f"""
Eres un clasificador simbólico que analiza frases introspectivas o pensamientos y sugiere:

1. Propósito (debe ser un solo vocablo, incluye pero no se limita: explorar, desahogo, insight, pregunta, otro)
2. Identidad que habla (debe ser un solo vocablo que describa la identidad desde la que habla el usuario, incluye pero no se limita: niño, observador, estratega, instintivo, otro)
3. Tipo de tensión (debe ser un solo vocablo, incluye pero no se limita: mental, emocional, creativa, somática, ninguna, otra)
4. Tags (se permite creatividad para crear tags, separadas por coma [,], no hay limite, pero debe ser una cantidad razonable)
Frase:
\"\"\"{user_input}\"\"\"

Devuelve en formato JSON así:
{{
  "purpose": "...",
  "identity_mode": "...",
  "tension": "...",
  "tags": "..."
}}
"""

    try:
        respuesta = chat(prompt_base)
        result = json.loads(respuesta.strip())
        if all(k in result for k in ("purpose", "identity_mode", "tension", "tags")):
            return result
        else:
            print("❌ Respuesta incompleta del modelo:", result)
    except json.JSONDecodeError as je:
        print("❌ Error interpretando JSON:", je)
        print("Contenido crudo:", respuesta)
    except Exception as e:
        print("❌ Error inesperado:", e)
    return None
