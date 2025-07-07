# Clarai - Módulo de Memoria Inteligente para H-Brain 🧠✨

**Clarai** es un módulo de inteligencia artificial diseñado para gestionar dinámicamente memorias operativas del usuario en el sistema H-Brain. Utiliza lenguaje natural para interpretar comandos, clasificar recuerdos y optimizar flujos cognitivos mediante embeddings semánticos.

---

## 🧩 Funciones Principales

- **add** ➕: Agrega memorias con categoría y relevancia
- **del** ❌: Elimina memorias por ID
- **rew** 🔄: Reescribe contenido, categoría o relevancia de una memoria
- **find** 🔍: Busca recuerdos relevantes por palabras clave
- **esc** 🕊️: Evalúa que no se requiere acción de memoria

---

## ⚙️ Estructura del Módulo

modulo_clarai/ 
├── ai_api.py           # Envío y procesamiento de mensajes con IA 
├── memory.py           # Lógica de almacenamiento y modificación de recuerdos 
├── history.py          # Historial de conversación por usuario y sesión 
├── run.py              # CLI del módulo Clarai 
├── tests/ 
│   └── test_clarai_flow.py  # Test funcional del ciclo completo 
└── README.md           # Este archivo

---

## 🗂️ Bases de Datos

- **clarai_memory.db**: Guarda los recuerdos clasificados (`id, resumen, categoría, relevancia`)
- **clarai_history.db**: Almacena historial de conversación por sesión (`usuario, mensaje, rol, timestamp`)

---

## 📦 Dependencias

- Python ≥ 3.10  
- Requiere acceso a `settings.json` en `~/H-Brain/configs/`  
- API externa de lenguaje (ej: DeepSeek, OpenAI) configurada en `clarai_api_url`  

---

## 🚀 Uso Rápido (CLI)

```bash
# Enviar un comando de memoria a Clarai:
PYTHONPATH=. python3 run.py UsuarioX 99 "add: Mem: Clarai gestiona recuerdos Cat: Clarai Relevancia: 9.0"

# Borrar una memoria:
PYTHONPATH=. python3 run.py UsuarioX 99 "del: 3"

# Buscar memorias relacionadas:
PYTHONPATH=. python3 run.py UsuarioX 99 "find: modularidad"


---

🧠 Principios de Diseño

IA autocurativa: Clarai puede identificar redundancias y fusionar memorias similares.

Embeddings eficientes: Usa text-embedding-3-small para comparar semánticamente recuerdos.

Aprendizaje continuo: Cada interacción refina el contenido almacenado, mejorando la asistencia.



---

📍 Próximas Integraciones

Conexión con NeuroBank para analizar costo/beneficio de tokens ↔ utilidad operativa

Métricas de precisión semántica con comparación entre estados previos y posteriores de memoria

Visor visual de memoria y líneas de tiempo desde SymContext



---

🧑‍💻 Autor

Hazael - Ingeniería Cognitiva y Sistemas IA Proyecto H-Brain 🌐
Desarrollado en Termux + Python, diseño modular.


---

