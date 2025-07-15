import unittest
from termux_backend.modules.modulo_symcontext.utils.classify_input import clasificar_input

class TestClasificarInput(unittest.TestCase):
    def test_clasificar_input_valido(self):
        texto = "Cuando me enfoco, logro claridad mental para avanzar"
        resultado = clasificar_input(texto)  # ← ESTA línea faltaba

        self.assertIsInstance(resultado, dict, "La clasificación debe retornar un diccionario")
        self.assertIn("purpose", resultado)
        self.assertIn("identity_mode", resultado)
        self.assertIn("tension", resultado)
        self.assertIn("emotion", resultado)
        self.assertIn("tags", resultado)
