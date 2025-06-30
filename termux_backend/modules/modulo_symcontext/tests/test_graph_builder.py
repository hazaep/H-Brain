import os
from termux_backend.modules.modulo_symcontext.analysis.graph_builder import generar_grafo_contextual

def test_generar_grafo_contextual():
    ruta = generar_grafo_contextual()
    
    assert ruta is not None, "La ruta devuelta por generar_grafo_contextual() es None"
    assert ruta.endswith(".png"), "El archivo generado no es un PNG"
    assert os.path.exists(ruta), f"No se encontró el archivo generado en la ruta: {ruta}"
