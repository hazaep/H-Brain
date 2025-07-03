import os
import json
from termux_backend.modules.modulo_clarai import ai_api, history, memory

username = "ClaraiDebugTest"
conv_id = 996

def test_send_and_memory():
    # Paso 1: Enviar mensaje inicial
    response = ai_api.send_message(username, conv_id, "Hola Clarai, ests es una prueba de tu memoria dinamica, porfavor colabora usando tus comandos tambien.")
    assert isinstance(response, str)
    print("[✓] Mensaje inicial enviado.")

    # Paso 2: Agregar memoria
    cmd = 'add: Mem: Clarai ayuda con memoria de IA Cat: Clarai Relevancia: 8.1'
    response = ai_api.send_message(username, conv_id, cmd)
    print("[✓] Memoria agregada.")

    # Paso 3: Buscar memoria agregada
    response = ai_api.send_message(username, conv_id, "busca modular con los comandos")
    assert "modular" in response or "Memoria" in response
    print("[✓] Búsqueda de memoria exitosa.")

    # Paso 4: Reescribir memoria
    conn_hist = history.init_history_db()
    conn_mem = memory.init_memory_db()
    user_id = history.get_or_create_user(conn_hist, username)
    mems = memory.search_memories(conn_mem, user_id, "modular")
    assert mems, "No se encontró memoria para reescribir"
    mem_id = mems[-1][0]  # Tomamos la última (más reciente)
    rew_cmd = f"reesctibre con un comando  {mem_id} Mem: Clarai fue actualizada Cat: Clarai Relevancia: 9.3"
    response = ai_api.send_message(username, conv_id, rew_cmd)
    print("[✓] Reescritura exitosa.")

# Paso 5: Confirmar cambios (debug temporal)
    print(f"[DEBUG] Se intentó actualizar la memoria con ID: {mem_id}")
    fila = memory.get_memory_by_id(mem_conn, mem_id)
    print("[DEBUG] Contenido después de rew:", fila)

    # Paso 5: Confirmar contenido directamente por ID
    cur = conn_mem.execute("SELECT summary FROM memories WHERE id=? AND user_id=?", (mem_id, user_id))
    row = cur.fetchone()
    assert row is not None, "No se encontró la memoria reescrita"
    assert "actualizada" in row[0], f"Memoria con ID {mem_id} no fue actualizada correctamente"
    print("[✓] Validación final exitosa.")

if __name__ == "__main__":
    test_send_and_memory()
    print("\n✅ Todo el flujo de Clarai funciona correctamente.")
