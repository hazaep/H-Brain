# termux_backend/modules/modulo_neurobank/main_neurobank.py

import argparse
import json
from termux_backend.modules.modulo_neurobank import neurobank
from termux_backend.modules.modulo_neurobank.utils import get_neurobank_db_path
from termux_backend.modules.modulo_neurobank.report_utils import (
    export_tokens_summary_csv,
    export_nfts_markdown
)

# Criptos registradas en el sistema pendiente setting.json
REGISTERED_CRYPTOS = {
    "NRN": "Neuron – Token principal del sistema",
    "SYNAP": "Synaptium – Token por uso de herramientas",
    "SYMCOIN": "Symbolic Coin – Módulo SymContext",
    "MOODBIT": "MoodBit – Módulo Bitácora",
    "AITHOUGHT": "AI Thought Token – Módulo IA",
    "Clarium": "Clarium – Módulo Clarai",
    "neuroNFT": "NeuroGem – NFT de introspección"
}

try:
    import readline
except ImportError:
    readline = None

def set_autocompleter(options):
    if readline:
        def completer(text, state):
            matches = [opt for opt in options if opt.startswith(text)]
            return matches[state] if state < len(matches) else None
        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")

def main():
    parser = argparse.ArgumentParser(
        description="🧠 NeuroBank CLI - Gestiona la economía simbólica de H-Brain"
    )
    subparsers = parser.add_subparsers(dest="comando")

    # 🔹 Mint Token
    p_mint_token = subparsers.add_parser("mint_token", help="Minar un nuevo token")
    p_mint_token.add_argument("module", help="Nombre del módulo que genera el token")
    p_mint_token.add_argument("action", help="Acción que genera el token")
    p_mint_token.add_argument("--amount", type=int, default=1, help="Cantidad a minar")
    p_mint_token.add_argument("--input_id", type=int, help="ID del input (opcional)")
    p_mint_token.add_argument("--crypto", default="NRN", help="Cripto asociada")
    p_mint_token.add_argument("--meta", help="Metadatos en formato JSON")

    # 🔹 Mint NFT
    p_mint_nft = subparsers.add_parser("mint_nft", help="Crear un nuevo NFT")
    p_mint_nft.add_argument("input_id", type=int, help="ID del input relacionado")
    p_mint_nft.add_argument("--title", help="Título opcional para el NFT")
    p_mint_nft.add_argument("--crypto", default="neuroNFT", help="Cripto asociada")
    p_mint_nft.add_argument("--meta", help="Metadatos en formato JSON")

    # 🔹 Ver Balance
    p_balance = subparsers.add_parser("balance", help="Ver balance total o por módulo")
    p_balance.add_argument("--module", help="Filtrar por módulo")

    # 🔹 Ver tokens
    p_tokens = subparsers.add_parser("list_tokens", help="Listar tokens minados")
    p_tokens.add_argument("--module", help="Filtrar por módulo")

    # 🔹 Ver NFTs
    subparsers.add_parser("list_nfts", help="Listar NFTs creados")

    # 📊 Reporte: tokens → CSV
    parser_report_tokens = subparsers.add_parser("report_tokens", help="Exportar resumen de tokens por módulo y acción a CSV")
    parser_report_tokens.add_argument("--out", help="Ruta de salida del archivo CSV", default="tokens_report.csv")

    # 🖼️ Reporte: NFTs → Markdown
    parser_report_nfts = subparsers.add_parser("report_nfts", help="Exportar lista de NFTs a Markdown")
    parser_report_nfts.add_argument("--out", help="Ruta de salida del archivo Markdown", default="nft_report.md")

    # 🔹 Modo interactivo
    subparsers.add_parser("interactive", help="Modo CLI interactivo")

    args = parser.parse_args()

    if not args.comando:
        parser.print_help()
        return

    # 🔁 Dispatch según comando
    if args.comando == "mint_token":
        metadata = {}
        if args.meta:
            try:
                metadata = json.loads(args.meta)
            except json.JSONDecodeError:
                print("⚠️ Metadatos mal formateados. Asegúrate de usar JSON válido.")
                return
        neurobank.mint_token(
            module=args.module,
            action=args.action,
            amount=args.amount,
            input_id=args.input_id,
            crypto=args.crypto,
            metadata=metadata
        )

    elif args.comando == "mint_nft":
        metadata = {}
        if args.meta:
            try:
                metadata = json.loads(args.meta)
            except json.JSONDecodeError:
                print("⚠️ Metadatos mal formateados. Asegúrate de usar JSON válido.")
                return
        neurobank.mint_nft(
            input_id=args.input_id,
            title=args.title,
            crypto=args.crypto,
            metadata=metadata
        )

    elif args.comando == "balance":
        total = neurobank.get_balance(module=args.module)
        print(f"📊 Balance total: {total}")

    elif args.comando == "list_tokens":
        neurobank.list_tokens(module=args.module)

    elif args.comando == "list_nfts":
        neurobank.list_nfts()

    elif args.comando == "report_tokens":
        export_tokens_summary_csv(args.out)

    elif args.comando == "report_nfts":
        export_nfts_markdown(args.out)

    elif args.comando == "interactive":
        print("=== 💠 MODO INTERACTIVO – NEUROBANK ===")

        while True:
            print("\nElige una opción:")
 #           print("1. 🪙 Minar token")
  #          print("2. 🖼️ Crear NFT")
   #         print("3. 📊 Ver balance")
    #        print("4. 📜 Ver historial de tokens")
     #       print("5. 🧾 Ver historial de NFTs")
      #      print("6. 🚪 Salir")

       #     opcion = input(">> ").strip()

            opciones = {
        "1": ("Ver balance total", lambda: print(f"📊 Balance total: {neurobank.get_balance()}")),
        "2": ("Listar tokens", neurobank.list_tokens),
        "3": ("Listar NFTs", neurobank.list_nfts),
        "4": ("Minar token", lambda: neurobank.mint_token(
            input("🔹 Módulo: "), input("🔸 Acción: "),
            int(input("💰 Cantidad: ")), None,
            json.loads(input("📎 Metadata (JSON): ") or "{}")
        )),
        "5": ("Crear NFT", lambda: neurobank.mint_nft(
            int(input("🔗 ID del input relacionado: ")),
            input("🎨 Título: "),
            input("📎 Metadata (JSON): ")
        )),
        "6": ("📤 Exportar resumen de tokens a CSV", lambda: export_tokens_summary_csv(
            input("📁 Ruta de salida (por defecto: tokens_report.csv): ") or "tokens_report.csv"
        )),
        "7": ("📝 Exportar NFTs a Markdown", lambda: export_nfts_markdown(
            input("📁 Ruta de salida (por defecto: nft_report.md): ") or "nft_report.md"
        )),
        "0": ("Salir", lambda: exit())
    }

            if opcion == "1":
                print("\n🪙 Minar token:")
                set_autocompleter(["symcontext", "modulo_ai", "bitacora", "clarai"])  # puedes usar settings.json para extenderlo
                module = input("🔧 Módulo: ")
                action = input("⚙️ Acción: ")
                amount = input("🔢 Cantidad (default 1): ").strip() or "1"
                input_id = input("🆔 ID de input (opcional): ").strip()
                print("\n🪙 Criptos registradas:")
                for code, desc in REGISTERED_CRYPTOS.items():
                    print(f"  - {code}: {desc}")
                set_autocompleter(list(REGISTERED_CRYPTOS.keys()))
                crypto = input("🪙 Cripto (default NRN): ").strip() or "NRN"
                meta = input("📎 Metadatos en JSON (opcional): ").strip()

                try:
                    amount = int(amount)
                    input_id = int(input_id) if input_id else None
                    metadata = json.loads(meta) if meta else {}
                    neurobank.mint_token(module, action, amount, input_id, crypto, metadata)
                except Exception as e:
                    print(f"❌ Error al minar token: {e}")

            elif opcion == "2":
                print("\n🖼️ Crear NFT:")
                input_id = input("🆔 ID de input: ")
                title = input("🏷️ Título (opcional): ").strip()
                print("\n🪙 Criptos registradas:")
                for code, desc in REGISTERED_CRYPTOS.items():
                    print(f"  - {code}: {desc}")
                crypto = input("💠 Cripto (default neuroNFT): ").strip() or "neuroNFT"
                meta = input("📎 Metadatos en JSON (opcional): ").strip()

                try:
                    input_id = int(input_id)
                    metadata = json.loads(meta) if meta else {}
                    neurobank.mint_nft(input_id, title, crypto, metadata)
                except Exception as e:
                    print(f"❌ Error al crear NFT: {e}")

            elif opcion == "3":
                module = input("🔍 Filtrar por módulo (deja vacío para total): ").strip()
                total = neurobank.get_balance(module if module else None)
                print(f"📊 Balance: {total}")

            elif opcion == "4":
                module = input("🔍 Filtrar por módulo (opcional): ").strip()
                neurobank.list_tokens(module if module else None)

            elif opcion == "5":
                neurobank.list_nfts()

            elif opcion == "6":
                print("👋 Saliendo del modo interactivo...")
                break
            else:
                print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
