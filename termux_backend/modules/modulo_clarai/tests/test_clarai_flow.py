# test_clarai_flow.py

import os
import json
from termux_backend.modules.modulo_clarai import ai_api, history, memory

username = "ClaraiTest"
conv_id = 99  # ID de prueba

def test_send_and_memory():
    # Paso 1: Enviar mensaje inicial
    response = ai_api.send_message(username, conv_id, "add: Mem: Usuario inicia prueba de memoria dinámica, depuracion prueba y error Cat: Clarai Relevancia: 8.5")
    assert isinstance(response, str)
    print("[✓] Mensaje inicial enviado.")

    # Paso 2: Agregar una memoria adicional para asegurar prueba
    response = ai_api.send_message(username, conv_id, "add: Mem: Clarai ayuda con memoria de IA, ayuda enviando comandos  Cat: Clarai Relevancia: 9.5")
    print("[✓] Memoria agregada.")

    # Paso 3: Buscar memorias relacionadas con la palabra clave
    response = ai_api.send_message(username, conv_id, "find: dinámica")
    assert "dinámica" in response or "Memoria" in response
    print("[✓] Búsqueda de memoria exitosa.")

    # Paso 4: Reescribir una memoria que contiene "dinámica"
    mem_conn = memory.init_memory_db()
    user_id = history.get_or_create_user(history.init_history_db(), username)
    mems = memory.search_memories(mem_conn, user_id, "dinámica")
    assert mems, f"No se encontró memoria con 'dinámica' para user_id={user_id}"

    mem_id = mems[0][0]
    rew_cmd = f"rew: {mem_id} Mem: Clarai fue actualizada, usa rew y del Cat: Clarai Relevancia: 9.3"
    response = ai_api.send_message(username, conv_id, rew_cmd)
    print("[✓] Reescritura exitosa.")

    # Paso 5: Confirmar cambios con impresión de depuración
    row = memory.get_memory_by_id(mem_conn, mem_id)
    print(f"[DEBUG] Contenido después de rew: {row}")
    assert "actualizada" in row[1], f"Memoria con ID {mem_id} no fue actualizada correctamente"
    print("[✓] Validación final exitosa.")

if __name__ == "__main__":
    test_send_and_memory()
    print("\n✅ Todo el flujo de Clarai funciona correctamente.")
