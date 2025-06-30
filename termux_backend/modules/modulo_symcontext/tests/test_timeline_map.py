import io
import sys
from termux_backend.modules.modulo_symcontext.analysis import timeline_map

def test_timeline_map_main():
    salida = io.StringIO()
    sys.stdout = salida

    try:
        timeline_map.main()
        output = salida.getvalue()
        assert "⏳" in output or "-" in output or "|" in output, "No parece haberse generado una línea de tiempo"
    finally:
        sys.stdout = sys.__stdout__
