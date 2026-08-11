# -*- coding: utf-8 -*-
"""
conftest.py — Configuración de pytest.

Agrega la raíz del proyecto al sys.path para que las pruebas
puedan importar app y modulos sin importar dónde se ejecuten.
"""

import os
import sys

# Ladrillo: variable con la ruta de la raíz del proyecto.
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ladrillo: condicional para añadir la raíz a la ruta de búsqueda de Python.
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZA)