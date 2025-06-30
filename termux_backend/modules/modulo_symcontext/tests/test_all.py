import unittest
import os
import sys

# Asegurar que el directorio raíz esté en sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Cargar todos los tests del directorio actual
def main():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir=os.path.dirname(__file__), pattern="test_*.py")
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)

if __name__ == "__main__":
    main()
