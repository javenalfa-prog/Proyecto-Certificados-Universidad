# -*- coding: utf-8 -*-
"""
modulos/cocina.py — LA COCINA: reglas de negocio y cruce de datos.

Contiene las funciones puras de cálculo y clasificación definidas en
AGENTS.md. La interfaz nunca decide nada: solo pide datos a esta cocina.

Política de casos borde (acordada con el usuario):
- Solo reciben certificado los estudiantes del maestro con evaluaciones.
- Los casos borde (sin evaluaciones, fuera del maestro, módulos faltantes)
  se reportan como inconsistencias, no entran en los contadores.
"""

from collections import defaultdict

# Ladrillo: VARIABLE constante con la cantidad máxima de módulos por programa.
MAX_MODULOS = 4


def calcular_promedio(notas):
    """FUNCIÓN: promedio según AGENTS.md (suma de Notas / módulos cursados).

    TIPO de retorno: float con el promedio.
    """
    suma = 0.0        # Ladrillo: VARIABLE acumuladora.
    cantidad = 0      # Ladrillo: VARIABLE contadora.
    # Ladrillo: BUCLE for que recorre la lista de notas.
    for nota in notas:
        suma += nota
        cantidad += 1
    # Ladrillo: CONDICIONAL por si la lista viene vacía (evitar dividir por 0).
    if cantidad == 0:
        return 0.0
    return suma / cantidad


def decidir_certificado(promedio, asistencia):
    """FUNCIÓN: decide el tipo de certificado según AGENTS.md.

    Reglas (los límites INCLUYEN el valor):
    - Aprobación    si Promedio >= 70 y Asistencia >= 80
    - Participación si Promedio < 70 y Asistencia >= 80
    - Sin certificado si Asistencia < 80
    TIPO de retorno: texto (str).
    """
    # Ladrillo: CONDICIONAL if/elif/else con las tres reglas.
    if promedio >= 70 and asistencia >= 80:
        return 'Aprobación'
    elif asistencia >= 80:
        return 'Participación'
    else:
        return 'Sin certificado'


def agrupar_por_estudiante_programa(evaluaciones):
    """FUNCIÓN: agrupa las evaluaciones por Identificacion + Programa.

    TIPO de retorno: diccionario clave (identificacion, programa) -> lista.
    """
    # Ladrillo: VARIABLE diccionario que agrupa por clave compuesta (tupla).
    grupos = defaultdict(list)
    # Ladrillo: BUCLE for que reparte cada evaluación en su grupo.
    for evaluacion in evaluaciones:
        clave = (evaluacion['identificacion'], evaluacion['programa'])
        grupos[clave].append(evaluacion)
    return grupos


def preparar_datos(estudiantes, evaluaciones):
    """FUNCIÓN principal de la cocina: cruza, calcula y clasifica.

    TIPO de retorno: diccionario con:
      - 'programas'      : lista de programas del maestro (para el filtro)
      - 'resultados'     : filas de estudiantes del maestro con evaluaciones
      - 'contadores'     : Aprobación / Participación / Sin certificado
      - 'inconsistencias': las tres listas de casos borde
    """
    # Ladrillo: VARIABLE índice para buscar el estudiante por su identificación.
    indice_estudiantes = {}
    for estudiante in estudiantes:  # Ladrillo: BUCLE for
        indice_estudiantes[estudiante['identificacion']] = estudiante

    # Ladrillo: VARIABLE conjunto con los ID del maestro.
    ids_maestro = set(indice_estudiantes.keys())

    # Ladrillo: VARIABLE conjunto con los ID que sí tienen evaluaciones.
    ids_evaluados = {e['identificacion'] for e in evaluaciones}

    # Ladrillo: llamada a la FUNCIÓN que agrupa por Identificacion + Programa.
    grupos = agrupar_por_estudiante_programa(evaluaciones)

    # Ladrillo: VARIABLE lista que irá juntando las filas de resultado.
    resultados = []
    # Ladrillo: VARIABLE diccionario que irá juntando las inconsistencias.
    inconsistencias = {
        'sin_evaluaciones': [],      # del maestro pero sin ninguna nota
        'fuera_del_maestro': [],     # evaluados que no están en el maestro
        'modulos_incompletos': [],   # grupos con menos de 4 módulos
    }

    # Ladrillo: BUCLE for sobre cada grupo (estudiante + programa).
    for (identificacion, programa), evaluaciones_grupo in grupos.items():
        # Ladrillo: VARIABLES listas con notas y asistencias del grupo.
        notas_grupo = [e['nota'] for e in evaluaciones_grupo]
        asistencias_grupo = [e['asistencia'] for e in evaluaciones_grupo]
        modulos_cursados = len(notas_grupo)

        # Ladrillo: CONDICIONAL para el caso "evaluado que no está en el maestro".
        if identificacion not in ids_maestro:
            inconsistencias['fuera_del_maestro'].append({
                'identificacion': identificacion,
                'programa': programa,
                'modulos': modulos_cursados,
            })
            continue  # Ladrillo: no entra en resultados (política acordada).

        # Ladrillo: CONDICIONAL para el caso "menos módulos de lo esperado".
        if modulos_cursados < MAX_MODULOS:
            inconsistencias['modulos_incompletos'].append({
                'identificacion': identificacion,
                'programa': programa,
                'modulos': modulos_cursados,
            })

        # Ladrillo: llamadas a las FUNCIONES de cálculo y decisión.
        promedio = calcular_promedio(notas_grupo)
        asistencia = calcular_promedio(asistencias_grupo)
        certificado = decidir_certificado(promedio, asistencia)

        # Ladrillo: CONDICIONAL para elegir la clase de color (presentación).
        if certificado == 'Aprobación':
            clase = 'aprobacion'
        elif certificado == 'Participación':
            clase = 'participacion'
        else:
            clase = 'sin-certificado'

        # Ladrillo: VARIABLE diccionario con la fila lista para la página.
        fila = {
            'identificacion': identificacion,
            'nombre': indice_estudiantes[identificacion]['nombre'],
            'programa': programa,
            'cohorte': indice_estudiantes[identificacion]['cohorte'],
            'modulos': modulos_cursados,
            'promedio': round(promedio, 2),
            'asistencia': round(asistencia, 2),
            'certificado': certificado,
            'clase': clase,
        }
        resultados.append(fila)

    # Ladrillo: BUCLE for con CONDICIONAL para detectar del maestro sin notas.
    for estudiante in estudiantes:
        if estudiante['identificacion'] not in ids_evaluados:
            inconsistencias['sin_evaluaciones'].append({
                'identificacion': estudiante['identificacion'],
                'nombre': estudiante['nombre'],
                'programa': estudiante['programa'],
            })

    # Ladrillo: ordenar por programa y nombre (función clave con sorted).
    resultados.sort(key=lambda f: (f['programa'], f['nombre']))

    # Ladrillo: VARIABLE contador de tipos de certificado (BUCLE for).
    contadores = {'aprobacion': 0, 'participacion': 0, 'sin_certificado': 0}
    for fila in resultados:
        if fila['certificado'] == 'Aprobación':
            contadores['aprobacion'] += 1
        elif fila['certificado'] == 'Participación':
            contadores['participacion'] += 1
        else:
            contadores['sin_certificado'] += 1

    # Ladrillo: VARIABLE lista con los programas únicos del maestro (ordenada).
    programas = sorted({e['programa'] for e in estudiantes})

    return {
        'programas': programas,
        'resultados': resultados,
        'contadores': contadores,
        'inconsistencias': inconsistencias,
    }
