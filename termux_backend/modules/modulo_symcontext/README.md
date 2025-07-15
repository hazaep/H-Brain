# 🧠 SymContext – Módulo de introspección simbiótica para H-Brain

El módulo **SymContext** permite registrar pensamientos introspectivos, analizarlos simbólicamente, encontrar patrones de transformación interna y detectar relaciones evolutivas. Es parte integral del sistema H-Brain y funciona tanto desde línea de comandos como desde otros módulos.

---

## ⚙️ Instalación y configuración

Este módulo depende de:

- Python 3.10+
- SQLite 3.40+
- Acceso a la API de IA configurada en `ai_router`
- Archivo de configuración `settings.json` con sección `"symcontext"`

```json
{
  "symcontext": {
    "sym_db_path": "termux_backend/database/context.db"
  }
}
```

---

## 🚀 Uso por CLI

Puedes ejecutar SymContext con:

```bash
symctx
```

### Menú interactivo

Al ejecutarlo sin argumentos, verás un menú con 12 opciones, como:

- Registrar input
- Ver entradas
- Buscar similares
- Mostrar bloques narrativos
- Detectar transiciones
- Ver configuración

---

## 🛠️ Comandos CLI directos

```bash
symctx registrar "Texto a registrar"
symctx similares "Texto de referencia"
symctx grafo
symctx timeline [--std]
symctx narrative [--std]
symctx transitions
symctx find_related "fragmento"
```

### Flags especiales

- `--std`: fuerza una salida estándar sin IA (solo para timeline y narrative)
- `--top N`: número de similares a mostrar (solo en similares)

---

## 🧬 Funcionalidades clave

### 1. Registro y clasificación automática

```bash
symctx registrar "Hoy aprendí que los errores también son maestros"
```

Automáticamente se clasifica por:
- Propósito (purpose)
- Identidad simbólica (identity_mode)
- Tensión (tension)
- Emoción (emotion)
- Embedding semántico (1536d)

### 2. Bloques narrativos (por default usa IA)

```bash
symctx narrative
symctx narrative --std 10
```

📘 **Análisis IA:**
- Detecta patrones temáticos
- Sugiere bloques coherentes
- Genera narrativa de transformación simbólica

### 3. Línea de vida simbólica

```bash
symctx timeline
symctx timeline --std 15
```

- 📈 **Vista IA:** muestra evolución de identidad simbólica en el tiempo
- 📜 **Vista estándar:** lista de entradas con íconos simbólicos

### 4. Transiciones simbólicas

```bash
symctx transitions
```

- 🚧 Detecta cambios significativos en propósito, identidad o tensión
- 🧠 Entrega análisis simbiótico de las etapas

### 5. Pensamientos similares (embedding)

```bash
symctx similares "Estoy en una etapa de mucha prueba"
```

- 🔎 Usa distancia coseno entre embeddings
- 📐 Muestra los más cercanos semánticamente

### 6. Relaciones simbólicas enriquecidas (con IA)

```bash
symctx find_related "las pruebas crean adaptacion"
```

- 🔗 Busca por similitud semántica usando embeddings
- 🧠 Genera un análisis simbiótico con IA
- 📁 Guarda automáticamente en: `termux_backend/database/related/TEXTO_140725-233245.md`

---

## 🧪 Pruebas IA integradas

```bash
symctx test_ai
```

Verifica si las funciones `chat()` y `embed()` están disponibles y operativas.

---

## 📚 Estructura del módulo

```
modulo_symcontext/
├── analysis/
│   ├── narrative_blocks.py
│   ├── timeline_map.py
│   ├── transitions_detect.py
│   ├── find_related.py
│   └── symbolic_analysis.py
├── utils/
│   ├── input.py
│   ├── view_entries.py
│   ├── semantic_search.py
├── main_symcontext.py
```

---

## 🧩 Integración futura

- Tokenización de entradas por NeuroBank
- Interfaz visual basada en líneas de tiempo simbólicas
- Evaluación semanal de patrones dominantes

---

## 📜 Licencia

Este módulo forma parte del proyecto privado H-Brain. Uso personal autorizado. No redistribuir sin permiso del autor.

---

## ✨ Autor

Desarrollado por: **Hazael Escandon**
