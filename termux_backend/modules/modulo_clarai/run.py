
import sys
from termux_backend.modules.modulo_clarai.history import init_history_db, get_or_create_user, add_message, fetch_history
from termux_backend.modules.modulo_clarai.ai_api import send_message

def main():
    if len(sys.argv) < 4:
        print("Uso: python run.py <usuario> <id_conversacion> <mensaje>")
        sys.exit(1)

    username = sys.argv[1]
    conv_id = int(sys.argv[2])
    user_input = " ".join(sys.argv[3:])
    # inicializa historial y usuario
    history_conn = init_history_db()
    user_id = get_or_create_user(history_conn, username)
    # agrega el input del usuario
    add_message(history_conn, conv_id, 'user', user_input)
    # procesa y obtiene respuesta
    respuesta = send_message(username, conv_id, user_input)
    print(respuesta)

if __name__ == "__main__":
    main()
