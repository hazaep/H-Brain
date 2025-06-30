# tests/test_save_input.py

import os
import sqlite3
import tempfile
import shutil
import pytest
from unittest.mock import patch

from termux_backend.modules.modulo_symcontext.utils.input import save_input, get_db_path

# Crear entorno de prueba temporal
@pytest.fixture
def entorno_db_temporal(monkeypatch):
    # Crear una base temporal vacía
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_context.db")

    # Crear tabla requerida
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE context_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            purpose TEXT,
            identity_mode TEXT,
            tension TEXT,
            tags TEXT,
            embedding TEXT
        )
    """)
    conn.commit()
    conn.close()

    # Parchear función get_db_path para usar la base temporal
    monkeypatch.setattr("termux_backend.modules.modulo_tools.utils.get_db_path", lambda: db_path)

    yield db_path

    # Limpiar
    shutil.rmtree(temp_dir)

# Test de flujo completo con entrada mockeada
def test_save_input_completo(entorno_db_temporal):
    entrada = "Aprendí más probando que estudiando teoría."

    with patch("builtins.input", side_effect=["s"]):  # Aceptar categorías sugeridas
        resultado = save_input(entrada)

    assert resultado is not None
    assert resultado["texto"] == entrada
    assert isinstance(resultado["id"], int)
    assert os.path.exists(resultado["grafo_path"])
