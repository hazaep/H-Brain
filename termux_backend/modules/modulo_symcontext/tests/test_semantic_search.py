import pytest
from termux_backend.modules.modulo_symcontext.utils.semantic_search import buscar_similares_emb

def test_buscar_similares_emb_valido(capsys):
    texto = "Cuando dudo, respiro y observo el pensamiento"
    buscar_similares_emb(texto)

    salida = capsys.readouterr().out
    assert "Más similares a" in salida or "Distancia" in salida, "La salida no contiene resultados de similitud"
