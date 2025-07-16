# termux_backend/modules/modulo_symcontext/docs/cheatsheet.py

def mostrar_cheat_sheet():
    print("""
🧠 SymContext — Guía Rápida (Cheat Sheet)
==========================================

🟩 Registrar entrada:
    symctx registrar "Hoy comprendí algo importante"

🔎 Buscar similares:
    symctx similares "me siento desbordado"

🧵 Buscar relaciones simbólicas:
    symctx find_related "estructura interna"

📚 Ver bloques narrativos:
    symctx narrative          → Análisis con IA
    symctx narrative --std    → Modo bloques puros

📈 Línea de vida introspectiva:
    symctx timeline           → Modo IA
    symctx timeline --std 10  → Últimas 10 entradas

🚧 Transiciones simbólicas:
    symctx transitions

🕸️ Generar grafo semántico:
    symctx grafo

🛠️ Verificar DB:
    symctx verificar_db

⚙️ Ver configuración actual:
    symctx config

🧪 Probar conexión IA:
    symctx test_ai

📂 Archivos IA relacionados:
    termux_backend/database/related/*.md

TIP: Ejecuta `symctx` solo para usar el menú interactivo.
""")

