#!/data/data/com.termux/files/usr/bin/bash

# Activar entorno virtual desde la raíz del proyecto
source ../venv/bin/activate

# Establecer variable para que Flask sepa dónde está la app
export FLASK_APP=api:app
export FLASK_ENV=development  # Opcional: muestra errores detallados

# Ejecutar Flask
flask run --host=127.0.0.1 --port=5000
