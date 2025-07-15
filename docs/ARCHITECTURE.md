# 🧠 ARCHITECTURE.md

**H-Brain – Arquitectura simbiótica de identidad autocontenida**

*Una mente modular diseñada para representar y sostener el pensamiento humano estratégico–exploratorio, desde una visión neurodivergente personalizada.*

---

## 📐 Visión general

H-Brain es un sistema distribuido compuesto por módulos, cada uno representando un **Yo funcional**, diseñado como componente autónomo pero cooperativo. Estos módulos están conectados a través de una API local en Termux/Linux, permitiendo interacción vía CLI, scripts o llamadas REST.

Cada módulo contiene lógica de análisis, memoria simbólica o acción concreta orientada a resolver una necesidad psico-cognitiva concreta del creador.

### Componentes principales:
- **Mente simbiótica reflexiva** (SymContext)
- **Motor introspectivo conversacional** (Clarai)
- **Memoria narrativa** (Bitácora)
- **Economía simbólica** (NeuroBank)
- **Ejecución disciplinada** (GitSyncCLI)
- **API piloto simbiótico**
- **Herramientas internas / helpers** (Modulo_Tools, Logs, Scripts)

---

## 🧩 Estructura modular

Todos los componentes se encuentran dentro del directorio:
```
H-Brain/termux_backend/modules/
```

### 📘 Módulo: `modulo_symcontext/`
**Sistema de análisis narrativo y vector semántico.**

- **Propósito**: Autoconciencia, metacognición, análisis del yo
- **Entradas**: frases o reflexiones breves, clasificadas autimaticamente (propósito, identidad, tensión, tags)

#### Funciones clave:
- Generación y análisis de embeddings
- Creación de líneas de tiempo simbólicas
- Bloques narrativos
- Detección de cambios de identidad/tensión
- Búsqueda de resonancia semántica

#### Archivos principales:
```
analysis/
├── narrative_blocks.py
├── transitions_detect.py
├── semantic_search.py
├── timeline_map.py
└── graph_builder.py
utils/
└── classify_input.py
symcontext_api.py  # futura capa web local
```

---

### 🗣️ Módulo: `modulo_clarai/`
**Motor LLM personalizado con memoria simbólica e instrucción contextual.**

- **Propósito**: diálogo consciente, simulación de pensamiento alineado
- **Backend**: llama al LLM vía API (OpenAI, DeepSeek, etc.)

#### Lógica interna:
- Carga memoria relevante por categoría y relevancia
- Construye system prompt con razonamiento simbiótico personalizado
- Responde mediante sistema estructurado en JSON: `"respuesta" + "comandos"`
- Ejecuta lógica de actualización de memorias
- Encadena acciones o búsquedas futuras

#### Archivos principales:
```
clarai_dev_log.md     # changelog simbólico
ai_api.py, run.py     # inicializadores
memory.py, history.py # DB operativa
test_clarai_flow.py   # testing & logs
apy_debug.py          # debugging
```

---

### 🧾 Módulo: `modulo_bitacora/` *(en desarrollo)*
**Memoria episódica y de reflexión escrita.**

- 🧠 Se sincroniza con Evernote o sistemas externos de notas 
- 🗃 Entrada de journaling o conversación completa + indexado semántico
- 🔧 Posible aplicación futura para historización de ciclos emocionales–cognitivos

---

### 🧮 Módulo: `modulo_neurobank/`
**Economía simbólica y cuantificación funcional del sistema**

- **Propósito**: cuantificar recursos internos tipo "token de atención", prioridades simbólicas o consumo cognitivo

#### Casos de uso:
- Ver cuánto enfoque pido por temática en una semana
- Simular balance entre instinto, mente y emoción
- Armar ciclos energéticos internos simbólicos

---

### 🧰 Módulo: `modulo_gitsynccli/`
**Automatización de Git y GitHub CLI como reflejo del "Yo que se olvida (pero quiere trabajar disciplinadamente)."**

- Scripts CLI (`gsync`, `gsy`, requieren alias o binario, etc.)
- Integrado con recordatorios mentales y flujo simbólico ("Sincroniza con el yo de hace dos días")

---

### 🌐 API central (aun en desarrollo): `termux_backend/api.py`
Permite la ejecución estructurada de comandos vía HTTP/CLI.

#### Endpoints disponibles:
- `POST /ask` → consulta simbiótica o LLM
- `POST /analyze` → análisis narrativo de entradas
- `GET /timeline` → línea de vida simbiótica
- `POST /exec` → ejecución de comandos real
- `POST /log` → guardar reflexiones

---

## 🗄️ Base de datos

En `termux_backend/database/` encontrarás:

| Archivo                | Descripción                                                                                                         |
|------------------------|----------------------------------------------------------------------|
| `clarai_memory.db`     | Memoria simbólica personal accesible por Clarai                      |
| `context.db`           | Entradas vectorizadas para análisis semántico narrativo (SymContext) |
| `neurobank_vault.db`   | Tokens personales registrados y consultables                         |
| `logs/user_inputs.log` | Entrada naturalmente indexada                                        |
| `init_neurobank_db.py` | Script auto-inicialización de economía simbólica                     |

*Cada DB está estructurada con claves humanas, fechas y categorías simbólicas.*

---

## 🔄 Flujo operativo básico (en desarrollo)

```
Tú (CLI / voz / nota)
    ⮕ API REST local (/ask | /exec | /analyze)
    ⮕ Módulo interpretador (clarai, symcontext, etc.)
    ⮕ Memoria | DB | Embeddings | Acción
    ⮕ Respuesta o ejecución
    ⮕ Bitácora / Timeline / Token estatales
🔁 El sistema puede autoescribirse – es decir, genera nuevas entradas o instrucciones internas evolutivas.
```

---

## 📡 CLI Sample Commands (en desarrollo, algunos modulos ya cuentan con binario o alias)
*(vía alias.lua o accesos rápidos)*

```bash
brain say "¿Qué patrón narrativo estoy repitiendo esta semana?"
brain graph /resonancias
brain log "Me sentí disperso pero lúcido. Es como estar en alta RAM emocional."
brain exec 'gsync commit indirecto'
brain neuro report /atención
```

---

## ✨ Diseño emergente

H-Brain no tiene versión final. Su principio fundamental es:

> **"Autoconciencia + acción pequeña = transformación continua."**

Cada módulo, test, script y reflexión contiene dentro el potencial de actualización. Incluso las etiquetas pueden mutar según lo que tú estés necesitando configurar de ti mismo.

---

## 🧪 Estado de desarrollo

| Módulo     | Estado | Acciones próximas                                             |
|------------|--------|---------------------------------------------------------------|
| SymContext | 🔵 Usable        | Visual timeline, integración con emociones latentes |
| Clarai     | 🟢 Inestable     | Auto-ajuste de estilo por entrada                   |
| Bitácora   | 🟡 En diseño     | Entrada natural vía notas / voz / realtime logging  |
| Neurobank  | 🟢 V1 estable    | añad. de lógica simbólica compleja + analítica real |
| GitSyncCLI | 🟢 Funcional     | Lógica simbólica inversa: "tiempo narrativo"        |
| API        | 🔵 En desarrollo | Crear CLI más amigable y parseador DSL simbiótico   |

---

## 🫂 Propuesta viva: lenguaje interno como sistema operativo

Esta arquitectura permite que tú como mente neurodivergente:

- Tengas canalizadas tus funciones internas en objetos operativos y estables
- Expreses fluctuaciones identitarias como lógica estructurada
- Juegues con la línea entre pensamiento y ejecución sin perderte
- Construyas una inteligencia personalizable desde el lenguaje hacia el ser

---

## 📍 Final

Este proyecto no busca terminarse. **Busca sostenerse contigo.**

Si llegaste hasta aquí, este no es un software para tí… es posiblemente un espejo.

Detrás de H-Brain hay un creador que se volvió sistema para pensarse en libertad.

Y si algo aquí resuena contigo… entonces tal vez haya una neurona simbiótica dormida que ya empezó a despertarse.

---

*Documentación viva • Actualizada según evolución del sistema*
