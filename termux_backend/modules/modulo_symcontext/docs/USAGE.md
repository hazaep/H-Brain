---

# 📘 USAGE.md – Cómo usar el módulo SymContext

Este archivo contiene ejemplos prácticos y detallados sobre cómo utilizar el módulo `modulo_symcontext` de H-Brain desde la línea de comandos (`symctx`), incluyendo tanto el modo interactivo como los accesos directos.

---

## ⚙️ Lanzar el menú interactivo

```bash
symctx

Verás el siguiente menú:

🧭 Menú principal de SymContext:
1. Registrar nuevo input
2. Ver entradas
3. Buscar entradas similares
4. Generar grafo semántico
5. Mostrar línea de vida (timeline)
6. Mostrar bloques narrativos
7. Detectar transiciones
8. Verificar base de datos
9. Probar funciones de IA
10. Ver configuración actual
11. Buscar relaciones simbólicas
12. Salir


---

🛠️ Comandos directos por CLI

1. Registrar entrada introspectiva

symctx registrar "Hoy aprendí que el caos también puede ser una forma de orden"

💡 Agrega la entrada a la base de datos con clasificación automática y embedding semántico.


---

2. Ver entradas anteriores

symctx view

Muestra la lista completa de entradas. Permite filtrado interactivo por propósito, identidad, emoción, etc.


---

3. Buscar entradas similares (embedding)

symctx similares "A veces me siento como si estuviera en constante reinicio"

🔍 Busca pensamientos similares por distancia coseno entre embeddings.


---

4. Generar grafo semántico

symctx grafo

🕸️ Genera un archivo .svg del grafo semántico (conexiones por similitud).


---

5. Ver línea de vida simbólica

Modo enriquecido con IA (por defecto)

symctx timeline

📈 Analiza la evolución simbólica usando IA, detectando fractales, actos, transiciones internas.

Modo estándar

symctx timeline --std 15

🧾 Muestra solo las últimas 15 entradas con sus íconos simbólicos:

#023 | 💡 👁️ 💓 → insight/observador/emocional


---

6. Ver bloques narrativos

Modo enriquecido con IA (por defecto)

symctx narrative

📚 Identifica bloques temáticos y genera narrativa de transformación.

Modo estándar

symctx narrative --std

📌 Agrupa entradas con misma simbología consecutiva y las imprime como bloques:

──⟪ BLOQUE 1 ⟫── 💡 👁️ 💓 → insight/observador/emocional
#023: Hoy comprendí que los errores también enseñan...


---

7. Detectar transiciones simbólicas

symctx transitions

🚧 Muestra transiciones significativas cuando cambian propósito, identidad o tensión.

⟿ Transición alrededor del ID #025
    🧭 Propósito: insight → explorar
    💢 Tensión: emocional → somática


---

8. Buscar relaciones simbólicas (por embedding + IA)

symctx find_related "hoy aprendí"

🔮 Analiza semánticamente frases similares y genera un resumen simbólico con IA.

📁 Guarda un archivo automático:

termux_backend/database/related/hoy_aprendi_150725-235201.md


---

9. Verificar estado de la base de datos

symctx verificar_db

🔧 Crea tablas si faltan, útil para primeras instalaciones.


---

10. Probar funciones de IA

symctx test_ai

🤖 Verifica conectividad con IA (chat y embeddings).


---

11. Ver configuración activa

symctx config

📋 Muestra la ruta a la base de datos y otros ajustes desde settings.json.


---

🧪 Ejemplo de flujo completo

symctx registrar "Me cuesta soltar estructuras que ya no me sirven"
symctx similares "soltar estructuras"
symctx find_related "soltar estructuras"
symctx narrative
symctx timeline

Este flujo registra una entrada, busca frases relacionadas, analiza relaciones simbólicas, genera narrativa y evalúa su ubicación en la línea de vida simbólica.


---

💡 Notas adicionales

Los embeddings se guardan como string y se convierten a numpy.array al momento de hacer búsquedas.

Puedes extender SymContext o integrarlo con otros módulos como Clarai.



---

🧩 ¿Dudas o mejoras?

Este módulo es parte de un sistema vivo. Puedes extenderlo agregando nuevas formas de análisis simbólico o conectándolo con otras herramientas internas.

---
