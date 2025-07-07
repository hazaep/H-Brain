import argparse
import json
import os
import subprocess
from termux_backend.modules.modulo_neurobank import neurobank
from termux_backend.modules.modulo_neurobank.reports import (
    export_tokens_summary_csv,
    export_nfts_markdown,
)

def termux_open_if_available(filepath):
    """Abre archivo con termux-open si se está en Termux y termux-api está disponible."""
    if os.environ.get("PREFIX") and shutil.which("termux-open"):
        print(f"📂 Abriendo archivo: {filepath}")
        subprocess.run(["termux-open", filepath])
    else:
        print(f"✅ Archivo exportado: {filepath}")

def modo_interactivo():
    print("\n🧠 Bienvenido al modo interactivo de NeuroBank:")
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
            json.loads(input("📎 Metadata (JSON): ") or "{}"),
            input("🔹 Módulo: ")
        )),
        "6": ("📤 Exportar resumen de tokens a CSV", lambda: (
            lambda path: (
                export_tokens_summary_csv(path),
                termux_open_if_available(path)
            ))(input("📁 Ruta de salida (por defecto: tokens_report.csv): ") or "tokens_report.csv")
        ),
        "7": ("📝 Exportar NFTs a Markdown", lambda: (
            lambda path: (
                export_nfts_markdown(path),
                termux_open_if_available(path)
            ))(input("📁 Ruta de salida (por defecto: nft_report.md): ") or "nft_report.md")
        ),
        "0": ("Salir", lambda: exit())
    }

    while True:
        print("\n📋 Opciones disponibles:")
        for key, (desc, _) in opciones.items():
            print(f" {key}. {desc}")
        seleccion = input("👉 Elige una opción: ").strip()
        if seleccion in opciones:
            try:
                opciones[seleccion][1]()
            except Exception as e:
                print(f"❌ Error al ejecutar la opción: {e}")
        else:
            print("⚠️ Opción no válida.")

def main():
    parser = argparse.ArgumentParser(description="🧠 NeuroBank CLI")
    subparsers = parser.add_subparsers(dest="comando")

    parser_balance = subparsers.add_parser("balance", help="Ver balance total")
    parser_balance.add_argument("--module", help="Filtrar por módulo")

    parser_mint = subparsers.add_parser("mint_token", help="Minar un token")
    parser_mint.add_argument("module")
    parser_mint.add_argument("action")
    parser_mint.add_argument("--amount", type=int, default=1)
    parser_mint.add_argument("--input_id", type=int, default=None)
    parser_mint.add_argument("--meta", default="{}")

    parser_nft = subparsers.add_parser("mint_nft", help="Crear un NFT")
    parser_nft.add_argument("input_id", type=int)
    parser_nft.add_argument("--title", default=None)
    parser_nft.add_argument("--meta", default="{}")
    parser_nft.add_argument("--module", required=True)

    subparsers.add_parser("list_tokens", help="Listar tokens")
    subparsers.add_parser("list_nfts", help="Listar NFTs")

    parser_csv = subparsers.add_parser("report_tokens", help="Exportar tokens como CSV")
    parser_csv.add_argument("--out", default="tokens_report.csv")

    parser_md = subparsers.add_parser("report_nfts", help="Exportar NFTs como Markdown")
    parser_md.add_argument("--out", default="nft_report.md")

    args = parser.parse_args()

    if not args.comando:
        return modo_interactivo()

    if args.comando == "balance":
        total = neurobank.get_balance(module=args.module)
        print(f"📊 Balance total: {total}")

    elif args.comando == "mint_token":
        neurobank.mint_token(
            module=args.module,
            action=args.action,
            amount=args.amount,
            input_id=args.input_id,
            metadata=json.loads(args.meta)
        )

    elif args.comando == "mint_nft":
        neurobank.mint_nft(
            input_id=args.input_id,
            title=args.title,
            metadata=json.loads(args.meta),
            module=args.module
        )

    elif args.comando == "list_tokens":
        neurobank.list_tokens()

    elif args.comando == "list_nfts":
        neurobank.list_nfts()

    elif args.comando == "report_tokens":
        export_tokens_summary_csv(args.out)
        termux_open_if_available(args.out)

    elif args.comando == "report_nfts":
        export_nfts_markdown(args.out)
        termux_open_if_available(args.out)

if __name__ == "__main__":
    main()
