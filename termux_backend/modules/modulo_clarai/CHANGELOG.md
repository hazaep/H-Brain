# 📜 CHANGELOG – Clarai (Módulo IA de H-Brain)

Historial de cambios del módulo `modulo_clarai`, parte del sistema H-Brain.

---

## [0.3.0] - 2025-07-03

### ✨ Mejoras
- Se agregó **soporte para múltiples comandos** por respuesta de IA (`"comando"` ahora puede ser una lista).
- Se ajustó el sistema para ejecutar varios comandos en orden y guardar la respuesta única en la historia.
- Se actualizó el `README.md` para reflejar nuevas funcionalidades.

### 🛠 Correcciones
- Se corrigió error `AttributeError: 'dict' object has no attribute 'strip'` cuando la IA devolvía un JSON ya interpretado.
- Se ajustó el parseo condicional según si `content` es `str` o `dict`.

---

## [0.2.1] - 2025-07-02

### ✨ Mejoras
- Se implementó test funcional `test_clarai_flow.py` que cubre todo el flujo: `add`, `rew`, `find`, `esc`, `del`.
- Se añadió retorno de `ID` desde el comando `add:` en la respuesta IA para mejor trazabilidad.
- La función `rewrite_memory()` ahora confirma y valida que los cambios fueron aplicados.

### 🐞 Correcciones
- Se solucionó bug donde `JSONDecodeError: Extra data` ocurría por múltiples objetos JSON concatenados.
- Se mejoró la resiliencia del parser `process_memory_command()` para strings incompletos o mal formateados.

---

## [0.2.0] - 2025-07-01

### ✨ Nuevas Funcionalidades
- Sistema completo de comandos desde IA (`add:`, `del:`, `rew:`, `find:`, `esc:`).
- Clasificación por categorías con relevancia ponderada.
- Base de datos `clarai_memory.db` con persistencia en SQLite.
- Interfaz por línea de comandos (`run.py`).

---

## [0.1.0] - 2025-06-28

### 🧪 Prototipo inicial
- Interfaz básica CLI.
- Conexión con API de IA (DeepSeek inicialmente).
- Manejo de usuarios y conversaciones (`history.py`).
- Lectura desde configuración centralizada `settings.json`.

---
