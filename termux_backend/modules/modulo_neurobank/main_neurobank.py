import argparse
from termux_backend.modules.modulo_neurobank import neurobank

def main():
    parser = argparse.ArgumentParser(
        description="💰 CLI de módulo NeuroBank – Registro de tokens y NFTs por actividad"
    )
    subparsers = parser.add_subparsers(dest="comando")

    # Comando: balance
    balance_parser = subparsers.add_parser("balance", help="Mostrar balance general o por módulo")
    balance_parser.add_argument("--module", "-m", help="Filtrar por nombre de módulo")

    # Comando: mint_token
    mint_token_parser = subparsers.add_parser("mint_token", help="Minar token")
    mint_token_parser.add_argument("module", help="Nombre del módulo")
    mint_token_parser.add_argument("action", help="Nombre de la acción")
    mint_token_parser.add_argument("--amount", "-a", type=int, default=1, help="Cantidad (default 1)")
    mint_token_parser.add_argument("--input_id", "-i", type=int, help="ID del input relacionado (opcional)")
    mint_token_parser.add_argument("--meta", help="Metadata en JSON (opcional)", default="{}")

    # Comando: mint_nft
    mint_nft_parser = subparsers.add_parser("mint_nft", help="Minar NFT")
    mint_nft_parser.add_argument("input_id", type=int, help="ID del input relacionado")
    mint_nft_parser.add_argument("--title", help="Título del NFT")
    mint_nft_parser.add_argument("--meta", help="Metadata en JSON (opcional)", default="{}")

    # Comando: list_tokens
    list_tokens_parser = subparsers.add_parser("list_tokens", help="Listar tokens")
    list_tokens_parser.add_argument("--module", "-m", help="Filtrar por módulo (opcional)")

    # Comando: list_nfts
    subparsers.add_parser("list_nfts", help="Listar NFTs")

    args = parser.parse_args()

    if args.comando == "balance":
        neurobank.get_balance(module=args.module)

    elif args.comando == "mint_token":
        import json
        metadata = json.loads(args.meta)
        neurobank.mint_token(
            module=args.module,
            action=args.action,
            amount=args.amount,
            input_id=args.input_id,
            metadata=metadata
        )

    elif args.comando == "mint_nft":
        import json
        metadata = json.loads(args.meta)
        neurobank.mint_nft(
            input_id=args.input_id,
            title=args.title,
            metadata=metadata
        )

    elif args.comando == "list_tokens":
        neurobank.list_tokens(module=args.module)

    elif args.comando == "list_nfts":
        neurobank.list_nfts()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
