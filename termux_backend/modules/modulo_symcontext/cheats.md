# 🧠 SymContext – Cheat Sheet 🧾

Guía rápida para usar el sistema de análisis simbólico de introspecciones en H-Brain desde terminal.

---

## 🧭 MENÚ PRINCIPAL

```bash
symctx
```

Abre menú interactivo para registrar, visualizar, buscar, analizar y generar insights.

---

## 🚀 COMANDOS RÁPIDOS

### ➕ Registrar entrada introspectiva

```bash
symctx registrar "Hoy comprendí que mis errores me pulen"
```

- Clasifica automáticamente propósito, identidad, tensión y emoción
- Genera embedding vectorial

### 👁️ Ver entradas registradas

```bash
symctx view
```

Filtra por campos simbólicos, tags o texto.

### 🔍 Buscar pensamientos similares (por embedding)

```bash
symctx similares "Necesito reestructurar mis hábitos"
```

- Usa distancia coseno entre embeddings
- Devuelve top 5 similares por defecto

### 🧵 Buscar relaciones simbólicas (con IA)

```bash
symctx find_related "estructura interna"
```

- Busca por similitud semántica
- Genera análisis con IA
- Guarda en: `database/related/estructura_interna_DDMMAA-HHMMSS.md`

### 🧱 Ver bloques narrativos

```bash
symctx narrative        # Modo IA enriquecido
symctx narrative --std  # Modo bloques simbólicos clásicos
```

### 📈 Ver línea de vida (timeline)

```bash
symctx timeline         # IA simbólica
symctx timeline --std 10  # Últimas 10 entradas codificadas
```

Ejemplo de salida:
```
#027 | 💡 👁️ 💓 → insight/observador/emocional
```

### 🚧 Detectar transiciones internas

```bash
symctx transitions
```

Muestra cambios de propósito, identidad o tensión en secuencia:

```
⟿ Transición alrededor del ID #019
    💢 Tensión: emocional → creativa
    👤 Identidad: niño → estratega
```

### 🕸️ Generar grafo semántico

```bash
symctx grafo
```

Crea un grafo `.svg` con nodos conectados por similitud semántica.

### 🛠️ Verificar DB (crea tablas si faltan)

```bash
symctx verificar_db
```

### 🧪 Probar conexión con IA

```bash
symctx test_ai
```

Verifica funciones `chat()` y `embed()` vía IA router.

### ⚙️ Ver configuración actual

```bash
symctx config
```

Muestra rutas activas desde `settings.json` (ej: `sym_db_path`)

---

## 🧩 CORTES RÁPIDOS

| Acción                       | Comando                     |
|------------------------------|-----------------------------|
| Registrar entrada            | `symctx registrar "..."`    |
| Ver entradas                 | `symctx view`               |
| Buscar similares             | `symctx similares "..."`    |
| Analizar narrativa simbólica | `symctx narrative`          |
| Ver línea de vida IA         | `symctx timeline`           |
| Línea estándar (últimos 15)  | `symctx timeline --std 15`  |
| Detectar transiciones        | `symctx transitions`        |
| Buscar relaciones simbólicas | `symctx find_related "..."` |
| Ver configuración            | `symctx config`             |
| Probar IA                    | `symctx test_ai`            |

---

## 📦 RUTAS CLAVE

- **Configuración**: `configs/settings.json`
- **Base de datos**: `termux_backend/database/context.db`
- **Embeddings**: campo `embedding` (como string)
- **Salida IA enriquecida**: `termux_backend/database/related/`

---

## 💬 Recordatorio

SymContext convierte introspecciones en patrones simbólicos que pueden ser:

- **Buscados** (por similitud)
- **Agrupados** (por coherencia interna)
- **Analizados** (por evolución narrativa)
- **Visualizados** (como grafo, timeline, bloques)

Cada input deja una huella que puede alimentar procesos IA internos o flujos con Clarai, NeuroBank o futuros módulos simbióticos.

---
