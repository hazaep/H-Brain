import os
import json
from termux_backend.modules.modulo_ai.ai_router import chat

def clasificar_input(user_input):
    prompt_base = f"""
Eres un clasificador simbólico que analiza frases introspectivas o pensamientos y sugiere:

1. Propósito (un solo vocablo ejemplos: explorar, desahogo, insight, pregunta, otro)
2. Identidad que habla (un solo vocabloej emplos: niño, observador, estratega, instintivo, otro)
3. Tipo de tensión (un solo vocablo ejemplos: mental, emocional, creativa, somática, ninguna, otra)
4. Emoción principal (un solo vocablo ejemplos: miedo, tristeza, enojo, alegría, sorpresa, calma, otra)
5. Tags (palabras clave separadas por coma, cantidad razonable)

Frase:
\"\"\"{user_input}\"\"\"

Devuelve en formato JSON así:
{{
  "purpose": "...",
  "identity_mode": "...",
  "tension": "...",
  "emotion": "...",
  "tags": "..."
}}
"""

    try:
        respuesta = chat(prompt_base)
        result = json.loads(respuesta.strip())
        if all(k in result for k in ("purpose", "identity_mode", "tension", "emotion", "tags")):
            return result
        else:
            print("❌ Respuesta incompleta del modelo:", result)
    except json.JSONDecodeError as je:
        print("❌ Error interpretando JSON:", je)
        print("Contenido crudo:", respuesta)
    except Exception as e:
        print("❌ Error inesperado:", e)
    return None
