#!/usr/bin/env python3
"""
main_symcontext.py — CLI para todas las herramientas de SymContext

Uso directo:
  symctx registrar "Texto a registrar" [--no-generate]
  symctx similares "Texto de referencia"
  symctx grafo
  symctx timeline
  symctx narrative [--std]
  symctx transitions
  symctx verificar_db
  symctx config
  symctx test_ai
  symctx find_related "fragmento"
------------------------------------------6

$ symctx --help

usage: main_symcontext [-h] {registrar,view,verificar_db,test_ai,config,grafo,timeline,narrative,transitions,find_related,similares} ...

optional arguments:
  -h, --help            show this help message and exit

comandos disponibles:
  registrar           Registrar un nuevo input
  view                Ver entradas registradas
  verificar_db        Verificar la base de datos SQLite
  test_ai             Probar los proveedores de IA configurados
  config              Mostrar configuración actual (settings.json)
  grafo               Generar grafo semántico actualizado
  timeline            Visualizar mapa temporal de entradas
  narrative           Detectar bloques narrativos
  transitions         Analizar transiciones simbólicas
  find_related        Buscar relaciones simbólicas a partir de un fragmento
  similares           Buscar pensamientos similares (por embeddings)
"""
import os
import json
import sys
import argparse
from pathlib import Path

# Ajuste de path para importar módulo
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR / "modules" / "modulo_symcontext"))

# Importaciones internas
from termux_backend.database.verify_or_init_db import cargar_schema_si_falta
from termux_backend.modules.modulo_tools.utils import get_settings
from termux_backend.modules.modulo_ai.ai_router import chat, embed

from utils.input import save_input
from utils.semantic_search import buscar_similares_emb
from utils.view_entries import main as view_entries_main
from analysis.graph_builder import generar_grafo_contextual
from analysis.timeline_map import main as timeline_map_main
from analysis.narrative_blocks import main as narrative_blocks_main
from analysis.transitions_detect import main as transitions_detect_main
from analysis.find_related import encontrar_relaciones_basicas


def ejecutar_menu_interactivo():
    opciones = [
        ("Registrar nuevo input", "registrar"),
        ("Ver entradas", "view"),
        ("Buscar entradas similares", "similares"),
        ("Generar grafo semántico", "grafo"),
        ("Mostrar línea de vida (timeline)", "timeline"),
        ("Mostrar bloques narrativos", "narrative"),
        ("Detectar transiciones", "transitions"),
        ("Verificar base de datos", "verificar_db"),
        ("Probar funciones de IA", "test_ai"),
        ("Ver configuración actual", "config"),
        ("Buscar relaciones simbólicas", "find_related"),
        ("Salir", "salir"),
    ]

    while True:
        print("\n🧭 Menú principal de SymContext:")
        for i, (desc, _) in enumerate(opciones, 1):
            print(f"{i}. {desc}")

        try:
            eleccion = int(input("Selecciona una opción (número): "))
            if eleccion < 1 or eleccion > len(opciones):
                raise ValueError()
        except ValueError:
            print("❌ Opción inválida.")
            continue

        comando = opciones[eleccion - 1][1]
        if comando == "salir":
            print("👋 Hasta luego.")
            break

        ejecutar_comando(comando)


def ejecutar_comando(comando, args=None):
    if comando == "registrar":
        texto = input("🗣️ ¿Qué quieres registrar ahora en SymContext?\n> ").strip()
        if not texto:
            print("⚠️ Texto vacío. Cancelado.")
            return
        # Respecta flag no-generate si viene vía args
        generar_grafo = not (args and getattr(args, "no_generate", False))
        info = save_input(texto, generar_grafo=generar_grafo)
        if not info:
            print("❌ Falló el registro.")
            return
        print("✅ Registro completado:")
        for k, v in info.items():
            print(f"  {k}: {v}")

    elif comando == "view":
        view_entries_main()

    elif comando == "similares":
        ref = input("🔍 Texto de referencia:\n> ").strip()
        if not ref:
            print("⚠️ Texto vacío. Cancelado.")
            return
        buscar_similares_emb(ref)

    elif comando == "grafo":
        path = generar_grafo_contextual()
        print(f"📍 Grafo generado en: {path}")

    elif comando == "timeline":
        use_std = getattr(args, "std", False)
        timeline_map_main(std=use_std)

#    elif comando == "timeline":
  #      timeline_map_main()

    elif comando == "narrative":
        use_std = getattr(args, "std", False)
        narrative_blocks_main(std=use_std)

    elif comando == "transitions":
        transitions_detect_main()

    elif comando == "verificar_db":
        cargar_schema_si_falta()

    elif comando == "test_ai":
        print("🤖 Probando función chat()")
        try:
            print("🧠 Respuesta:", chat("Hola, ¿cómo estás?"))
        except Exception as e:
            print("❌ Error en chat():", e)
        print("\n🔍 Probando función embed()")
        try:
            emb = embed("Texto de prueba para embedding.")
            print(f"📐 Embedding recibido ({len(emb)} dimensiones)")
        except Exception as e:
            print("❌ Error en embed():", e)

    elif comando == "config":
        print("🧾 Configuración actual:")
        try:
# Cargar configuración del módulo SymContext
            _cfg = get_settings()
            sym_cfg = _cfg.get("symcontext", {})
            for k, v in sym_cfg.items():
                print(f"{k}: {v}")
        except Exception as e:
            print("❌ Error leyendo settings.json:", e)

    elif comando == "find_related":
        ref = input("🧶 Fragmento del texto base:\n> ").strip()
        if not ref:
            print("⚠️ Texto vacío.")
            return
        encontrar_relaciones_basicas(ref)

    else:
        print(f"❌ Comando desconocido: {comando}")


def main():
    parser = argparse.ArgumentParser(prog="symctx")
    sub = parser.add_subparsers(dest="command")

    sub_reg = sub.add_parser("registrar", help="Registrar un nuevo input")
    sub_reg.add_argument("texto", nargs="?", help="Texto a registrar")
    sub_reg.add_argument(
        "--no-generate",
        action="store_true",
        help="No regenerar grafo tras el registro"
    )

    sub_nrtv = sub.add_parser("narrative", help="Bloques evolutivos narrativos")
    sub_nrtv.add_argument(
        "--std",
        action="store_true",
        help="Usar salida estándar en bloques (sin IA)"
    )

    sub_time = sub.add_parser("timeline", help="Mostrar línea de vida simbólica")
    sub_time.add_argument("--std", action="store_true", help="Usar salida estándar (sin IA)")

    sub_rel = sub.add_parser("find_related", help="Buscar relaciones simbólicas")
    sub_rel.add_argument("texto", help="Texto de referencia")

    sub_sim = sub.add_parser("similares", help="Buscar entradas similares")
    sub_sim.add_argument("texto", help="Texto de referencia")
    sub_sim.add_argument("--top", type=int, default=5, help="Número de similares")

    sub.add_parser("view", help="Ver todas las entradas o filtrar")
    sub.add_parser("verificar_db", help="Crear/actualizar tablas de DB")
    sub.add_parser("test_ai", help="Probar router AI (chat/embed)")
    sub.add_parser("config", help="Mostrar configuración actual")
    sub.add_parser("grafo", help="Generar grafo semántico")
    sub.add_parser("transitions", help="Detectar transiciones")

#    args = parser.parse_args()
#    if not args.command:
#        ejecutar_menu_interactivo()

    if len(sys.argv) == 1:
        ejecutar_menu_interactivo()
        return
    else:
        args = parser.parse_args()

#    else:
        # CLI directo: si el comando admite texto como argumento, úsalo
        if args.command in ("registrar", "similares", "find_related", "narrative", "timeline" ):
            # Si se pasó por CLI el texto, sobreescribe el prompt
            texto_cli = getattr(args, "texto", None)
            if texto_cli:
                # Inyectamos la entrada directamente
                if args.command == "registrar":
                    info = save_input(texto_cli, generar_grafo=not args.no_generate)
                    if info:
                        print("✅ Registro completado:")
                        for k, v in info.items():
                            print(f"  {k}: {v}")
                    return
                elif args.command == "similares":
                    buscar_similares_emb(texto_cli)
                    return
                elif args.comando == "narrative":
                    use_std = texto_cli
                    narrative_blocks_main(std=use_std)
                elif comando == "timeline":
                    use_std = texto_cli
                    timeline_map_main(std=use_std)
                else:
                    encontrar_relaciones_basicas(texto_cli)
                    return

        # Para el resto, llamamos a ejecutar_comando
        ejecutar_comando(args.command, args)


if __name__ == "__main__":
    main()
