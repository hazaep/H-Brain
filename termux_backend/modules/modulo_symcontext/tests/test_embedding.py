import unittest
from termux_backend.modules.modulo_symcontext.utils.embedding import obtener_embedding

class TestObtenerEmbedding(unittest.TestCase):
    def test_obtener_embedding_valido(self):
        texto = "Este es un ejemplo para probar el embedding."
        embedding = obtener_embedding(texto)  # ← ESTA línea faltaba

        self.assertIsInstance(embedding, list, "El resultado debe ser una lista")
        self.assertGreater(len(embedding), 0, "El embedding no debe estar vacío")
