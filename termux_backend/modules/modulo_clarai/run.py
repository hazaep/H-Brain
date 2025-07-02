import sys
from termux_backend.modules.modulo_clarai.ai_api import send_message

def main():
    if len(sys.argv) < 4:
        print("Uso: run.py <usuario> <id_conversacion> <mensaje>")
        sys.exit(1)
    user, conv, *msg = sys.argv[1:]
    print(send_message(user, int(conv), " ".join(msg)))

if __name__ == "__main__":
    main()
