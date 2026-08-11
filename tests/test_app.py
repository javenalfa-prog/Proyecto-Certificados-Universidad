# -*- coding: utf-8 -*-
"""
tests/test_app.py — Pruebas de la página web (el salón).

Usa el cliente de prueba de Flask para verificar que la página
muestra los contadores esperados, la tabla con colores y las
inconsistencias, sin necesidad de arrancar el servidor.
"""

# Ladrillo: importar la aplicación Flask del servidor.
from app import app


def test_pagina_principal_muestra_titulo_y_contadores():
    # Ladrillo: VARIABLE con el cliente de prueba de Flask.
    cliente = app.test_client()
    respuesta = cliente.get('/')

    # Ladrillo: CONDICIONAL del estado HTTP (200 = correcto).
    assert respuesta.status_code == 200

    # Ladrillo: obtener el HTML como texto para buscar contenido.
    texto = respuesta.get_data(as_text=True)

    # Ladrillo: contadores esperados (19/3/1) dentro de las tarjetas.
    assert 'Academia Horizonte' in texto
    assert '>19<' in texto                      # aprobación
    assert '>3<' in texto                       # participación
    assert '>1<' in texto                       # sin certificado
    assert 'Certificados de Aprobación' in texto
    assert 'Estudiantes sin certificado' in texto


def test_pagina_muestra_camila_verde_y_promedio():
    # Ladrillo: Camila Rojas debe estar en verde (clase aprobacion) con 91.25.
    cliente = app.test_client()
    texto = cliente.get('/').get_data(as_text=True)

    # Ladrillo: la fila lleva la clase de color asignada por la cocina.
    assert 'fila-aprobacion' in texto
    assert 'Rojas Mendez Camila' in texto
    assert '91.25' in texto
    assert '96.25' in texto


def test_pagina_muestra_inconsistencias():
    # Ladrillo: la sección de inconsistencias debe aparecer con los casos.
    cliente = app.test_client()
    texto = cliente.get('/').get_data(as_text=True)

    assert 'Inconsistencias detectadas' in texto
    assert '304560321' in texto   # maestro sin evaluaciones
    assert '999880777' in texto   # evaluado fuera del maestro
    assert 'Grupos con menos de 4 módulos (8)' in texto


def test_filtro_por_programa():
    # Ladrillo: al filtrar Excel, no debe aparecer un estudiante de IA.
    cliente = app.test_client()
    from urllib.parse import quote

    # Ladrillo: variable con el programa filtrado (codificado para la URL).
    programa = 'Excel Avanzado para Negocios'
    respuesta = cliente.get('/?programa=' + quote(programa))
    texto = respuesta.get_data(as_text=True)

    assert respuesta.status_code == 200
    assert 'Rojas Mendez Camila' not in texto   # es del programa IA
    assert 'Barboza Nunez Oscar' in texto        # es de Excel
    assert 'mostrando-col' in texto or f'Mostrando' in texto