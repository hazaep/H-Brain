import io
import sys
from termux_backend.modules.modulo_symcontext.analysis import transitions_detect

def test_transitions_detect_main():
    salida = io.StringIO()
    sys.stdout = salida

    try:
        transitions_detect.main()
        output = salida.getvalue()
        assert "➡️" in output or "→" in output or "transición" in output.lower(), "No se detectaron transiciones visibles"
    finally:
        sys.stdout = sys.__stdout__
