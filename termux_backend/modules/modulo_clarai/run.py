import sys
from termux_backend.modules.modulo_clarai.ai_api import send_message

def main():
    if len(sys.argv) < 4:
        print("Uso: run.py <usuario> <id_conversacion> <mensaje>")
        sys.exit(1)
    user, conv, *msg = sys.argv[1:]
#    print(send_message(user, int(conv), " ".join(msg)))
    answer, raw_comandos=send_message(user, int(conv), " ".join(msg))
    print(f"\n\n [ &Clarai> ] {answer}\n")
    n_com = 0
    print("___[IA-CLI]_______________________________________")
    for c in raw_comandos:
        print(f" [ &Clarai> {c}]")
    print(f"_________________________________[{user} CLI]: [✓]\n\n")


if __name__ == "__main__":
    main()
