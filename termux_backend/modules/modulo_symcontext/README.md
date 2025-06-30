# SymContext

**SymContext** es el módulo de introspección y registro de pensamientos de **H-Brain**, diseñado para capturar, organizar y conectar reflexiones, preguntas e insights mediante técnicas de clasificación automatizada, embeddings semánticos y visualizaciones narrativas.

---

## 📖 Descripción

SymContext permite al usuario:

1. **Registrar** entradas (frases, preguntas, insights) de forma interactiva o mediante API REST.  
2. **Clasificar** automáticamente cada entrada en tres dimensiones:
   - **Propósito** (`purpose`): explorar, desahogo, insight, pregunta u otro.  
   - **Identidad** (`identity_mode`): niño, observador, estratega, instintivo, filósofo, etc.  
   - **Tensión** (`tension`): mental, emocional, creativa, somática, ninguna u otra.

3. **Generar embeddings** semánticos con un proveedor de IA (p. ej. OpenAI) y almacenarlos en SQLite.  
4. **Buscar** entradas semánticamente similares para relevar patrones y resonancias internas.  
5. **Construir un grafo** contextual de conexiones entre entradas afines.  
6. **Visualizar** tu “línea de vida simbólica” en ASCII, con iconos que codifican propósito, identidad y tensión.  
7. **Detectar transiciones** significativas cuando cambian tus patrones internos (bloques narrativos).  

---

## 🔧 Requisitos faltan dependencias

- **Python 3.10+**  
- **SQLite** (incluido en Python estándar)  
- **Termux** (Android) o cualquier terminal Linux/macOS  
- Una **API Key** para embeddings (configurable via `settings.json`)

---

## 🗄️ Estructura del módulo

```text
modulo_symcontext/
├── analysis/                  # Scripts de análisis y visualización
│   ├── graph_builder.py       # Grafo contextual (NetworkX + matplotlib)
│   ├── timeline_map.py        # Línea de vida ASCII
│   ├── narrative_blocks.py    # Agrupación en bloques evolutivos
│   ├── transitions_detect.py  # Detección de transiciones
│   └── find_related.py        # Relaciones básicas por campos simbólicos
│
├── utils/                     # Funciones auxiliares y wrappers de IA
│   ├── classify_input.py      # Clasificador simbólico (OpenAI Chat)
│   ├── embedding.py           # Obtención y caching de embeddings
│   ├── semantic_search.py     # Búsqueda de entradas similares
│   ├── input.py               # Flujo de registro (`save_input()`)
│   └── view_entries.py        # Mostrar entradas y filtros
│
├── tests/                     # Tests unitarios / funcionales (pytest & unittest)
│
├── main_symcontext.py         # CLI (modo interactivo y comandos directos)
├── symcontext_api.py          # API Flask mínima para integraciones externas
├── context.db                 # Base de datos SQLite (generada en runtime)
├── settings.json              # Configuración de proveedor IA, rutas, flags
└── secrets/
    └── openai_key.txt         # Clave privada de OpenAI (o provider)

