# -*- coding: utf-8 -*-
"""
tests/test_cocina.py — Pruebas de las reglas de negocio (la cocina).

Cubre casos límite, promedio sobre pocos módulos y los conteos
esperados con los datos reales (19 Aprobación / 3 Participación /
1 Sin certificado, y Camila Rojas con 91.25).
"""

# Ladrillo: importar las funciones de la cocina y la bodega.
from modulos.bodega import cargar_estudiantes, cargar_evaluaciones
from modulos.cocina import calcular_promedio, decidir_certificado, preparar_datos


# ------------------------------------------------------------------
# Pruebas de calcular_promedio
# ------------------------------------------------------------------
def test_promedio_con_varias_notas():
    # Ladrillo: promedio = suma / cantidad de módulos cursados.
    assert calcular_promedio([80, 90, 100]) == 90.0


def test_promedio_vacio_devuelve_cero():
    # Ladrillo: condicional para no dividir entre cero.
    assert calcular_promedio([]) == 0.0


def test_promedio_tres_modulos():
    # Ladrillo: promedia sobre los módulos cursados (3), no sobre 4.
    assert calcular_promedio([90, 80, 70]) == 80.0


# ------------------------------------------------------------------
# Pruebas del decidir_certificado (límites incluidos)
# ------------------------------------------------------------------
def test_aprobacion_cuando_promedio_70_y_asistencia_80():
    # Ladrillo: los límites INCLUYEN el valor (aprueba con 70 y 80 exactos).
    assert decidir_certificado(70.0, 80.0) == 'Aprobación'


def test_participacion_cuando_promedio_bajo_y_asistencia_80():
    # Ladrillo: promedio menor a 70 con asistencia 80 -> participación.
    assert decidir_certificado(69.99, 80.0) == 'Participación'


def test_participacion_cuando_asistencia_justa():
    # Ladrillo: asistencia exactamente 80 incluye (no es sin certificado).
    assert decidir_certificado(50.0, 80.0) == 'Participación'


def test_sin_certificado_cuando_asistencia_baja():
    # Ladrillo: asistencia 79.99 es menor a 80 -> sin certificado.
    assert decidir_certificado(95.0, 79.99) == 'Sin certificado'


# ------------------------------------------------------------------
# Pruebas con los datos reales de Insumos/
# ------------------------------------------------------------------
def test_conteo_certificados_reales():
    # Ladrillo: leer los archivos reales y preparar los datos.
    estudiantes = cargar_estudiantes()
    evaluaciones = cargar_evaluaciones()
    datos = preparar_datos(estudiantes, evaluaciones)

    # Ladrillo: los contadores esperados según la política "solo maestro".
    # (el evaluado fuera del maestro 999880777 no cuenta).
    assert datos['contadores'] == {
        'aprobacion': 19,
        'participacion': 3,
        'sin_certificado': 1,
    }


def test_camila_rojas_aprobada_91_25():
    # Ladrillo: Camila Rojas (101230456) debe aprobar con 91.25 y asistencia 96.25.
    estudiantes = cargar_estudiantes()
    evaluaciones = cargar_evaluaciones()
    datos = preparar_datos(estudiantes, evaluaciones)

    # Ladrillo: bucle for con condicional para localizar la fila por ID.
    fila_camila = None
    for fila in datos['resultados']:
        if fila['identificacion'] == '101230456':
            fila_camila = fila
            break

    assert fila_camila is not None
    # Ladrillo: condicionales del criterio de éxito.
    assert fila_camila['promedio'] == 91.25
    assert fila_camila['asistencia'] == 96.25
    assert fila_camila['certificado'] == 'Aprobación'
    assert fila_camila['clase'] == 'aprobacion'


def test_inconsistencias_reales():
    # Ladrillo: las tres inconsistencias esperadas.
    estudiantes = cargar_estudiantes()
    evaluaciones = cargar_evaluaciones()
    datos = preparar_datos(estudiantes, evaluaciones)
    inc = datos['inconsistencias']

    # Ladrillo: un maestro sin evaluaciones, un fuera del maestro,
    # y ocho grupos con menos de 4 módulos.
    assert len(inc['sin_evaluaciones']) == 1
    assert inc['sin_evaluaciones'][0]['identificacion'] == '304560321'

    assert [e['identificacion'] for e in inc['fuera_del_maestro']] == ['999880777']

    assert len(inc['modulos_incompletos']) == 8


def test_todos_los_resultados_son_del_maestro():
    # Ladrillo: con la política elegida, ningún resultado debe ser ajeno al maestro.
    estudiantes = cargar_estudiantes()
    evaluaciones = cargar_evaluaciones()
    datos = preparar_datos(estudiantes, evaluaciones)

    ids_maestro = {e['identificacion'] for e in estudiantes}
    # Ladrillo: comprobar que toda fila proviene del maestro (bucle + condición).
    for fila in datos['resultados']:
        assert fila['identificacion'] in ids_maestro