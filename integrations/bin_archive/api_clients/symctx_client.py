import requests
import json
import argparse

# === Configuración ===
BASE_URL = "http://127.0.0.1:8000"   # Cambia esto si se expone por red local
API_TOKEN = "MiTokenSuperSecreto123"  # Token que definiste en settings.json

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}


# === Funciones para consumir endpoints ===

def registrar(texto):
    payload = {"texto": texto}
    r = requests.post(f"{BASE_URL}/symctx/register", headers=HEADERS, json=payload)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def ver_config():
    r = requests.get(f"{BASE_URL}/symctx/config", headers=HEADERS)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def ver_entradas():
    r = requests.get(f"{BASE_URL}/symctx/view", headers=HEADERS)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def buscar_similares(texto, top_n=5):
    payload = {"texto": texto, "top_n": top_n}
    r = requests.post(f"{BASE_URL}/symctx/similares", headers=HEADERS, json=payload)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def narrativa():
    r = requests.post(f"{BASE_URL}/symctx/narrative", headers=HEADERS)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def transiciones():
    r = requests.post(f"{BASE_URL}/symctx/transitions", headers=HEADERS)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def find_related(texto, top_n=5):
    payload = {"texto": texto, "top_n": top_n}
    r = requests.post(f"{BASE_URL}/symctx/find_related", headers=HEADERS, json=payload)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))


# === CLI ===

def main():
    parser = argparse.ArgumentParser(description="Cliente SymContext API")
    sub = parser.add_subparsers(dest="cmd")

    sub_reg = sub.add_parser("registrar", help="Registrar nuevo texto")
    sub_reg.add_argument("texto", help="Texto a registrar")

    sub_sim = sub.add_parser("similares", help="Buscar pensamientos similares")
    sub_sim.add_argument("texto", help="Texto base")
    sub_sim.add_argument("--top", type=int, default=5)

    sub_find = sub.add_parser("find_related", help="Buscar relaciones simbólicas + IA")
    sub_find.add_argument("texto", help="Texto base")
    sub_find.add_argument("--top", type=int, default=5)

    sub.add_parser("narrative", help="Análisis narrativo simbólico")
    sub.add_parser("transitions", help="Análisis simbólico de transiciones")
    sub.add_parser("view", help="Ver todas las entradas")
    sub.add_parser("config", help="Ver configuración")

    args = parser.parse_args()

    if args.cmd == "registrar":
        registrar(args.texto)
    elif args.cmd == "similares":
        buscar_similares(args.texto, args.top)
    elif args.cmd == "find_related":
        find_related(args.texto, args.top)
    elif args.cmd == "narrative":
        narrativa()
    elif args.cmd == "transitions":
        transiciones()
    elif args.cmd == "view":
        ver_entradas()
    elif args.cmd == "config":
        ver_config()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
