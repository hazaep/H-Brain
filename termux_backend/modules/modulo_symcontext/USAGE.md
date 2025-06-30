📚 Uso


CLI interactivo

```
cd ~/H-Brain
PYTHONPATH=. python3 termux_backend/modules/modulo_symcontext/main_symcontext.py

```
Selecciona en el menú:
1. Registrar
2. Ver entradas
3. Buscar similares
4. Generar grafo
5. Timeline ASCII
6. Bloques narrativos
7. Detectar transiciones
8. Verificar DB
9. Test IA
10. Ver config
11. Find related
12. Salir

CLI directo

```
# Registrar
PYTHONPATH=. python3 main_symcontext.py registrar "Tu reflexión aquí"
# Ver entradas
PYTHONPATH=. python3 main_symcontext.py view
# Timeline
PYTHONPATH=. python3 main_symcontext.py timeline
# Similares
PYTHONPATH=. python3 main_symcontext.py similares "palabras clave"

```

API REST

```
cd ~/H-Brain
PYTHONPATH=. python3 termux_backend/modules/modulo_symcontext/symcontext_api.py

```
- GET / → Info básica y endpoints.
- POST /registrar
  
- GET /timeline → JSON con líneas de vida.
- GET /grafo → JSON con ruta grafo_path.
- GET /similares?texto=... → JSON con lista de similares.
---

🧪 Testing

```
cd ~/H-Brain
PYTHONPATH=. pytest termux_backend/modules/modulo_symcontext/tests/
# o para unittest master:
python3 termux_backend/modules/modulo_symcontext/tests/test_all.py

```

---

🤝 Contribuir

1. Haz un fork.
2. Crea tu rama (git checkout -b feature/nueva-función).
3. Añade tests y documentación.
4. Envía un pull request.
