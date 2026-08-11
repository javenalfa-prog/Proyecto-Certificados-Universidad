# -*- coding: utf-8 -*-
"""
validar.py — Cruce y análisis de datos (Etapa 1 del PLAN.md).

Usa la misma lógica de la cocina (modulos/) para mostrar en consola:
resumen general, tabla completa por estudiante+programa e inconsistencias.
"""

import sys
from collections import defaultdict

# Ladrillo: importar la lógica de la cocina (un solo lugar de verdad).
from modulos.bodega import cargar_estudiantes, cargar_evaluaciones
from modulos.cocina import preparar_datos

# Ladrillo: FUNCIÓN que prepara la consola para mostrar acentos (UTF-8).
def preparar_consola():
    """Fuerza salida UTF-8 en Windows para que no salgan caracteres raros."""
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def main():
    """Ladrillo: FUNCIÓN principal que orquesta todo."""
    # 1) Leer los dos archivos (Bodega).
    estudiantes = cargar_estudiantes()
    evaluaciones = cargar_evaluaciones()

    # ------------------------------------------------------------------
    # 2) RESUMEN GENERAL
    # ------------------------------------------------------------------
    print('=' * 70)
    print('1) RESUMEN GENERAL')
    print('=' * 70)

    # Estudiantes por programa (maestro).
    # Ladrillo: VARIABLE diccionario (contador) + BUCLE for.
    conteo_programa = defaultdict(int)
    for e in estudiantes:
        conteo_programa[e['programa']] += 1
    print('Estudiantes por programa (maestro):')
    for programa, cantidad in sorted(conteo_programa.items()):
        print(f'   {programa}: {cantidad}')
    print(f'   Total: {len(estudiantes)}')

    # Cantidad de evaluaciones, módulos existentes y rango de notas.
    # Ladrillo: VARIABLES y conjuntos para valores únicos.
    modulos_existentes = sorted({e['modulo'] for e in evaluaciones})
    notas = [e['nota'] for e in evaluaciones]
    print(f'\nEvaluaciones (filas): {len(evaluaciones)}')
    print('Módulos existentes: ' + ', '.join(modulos_existentes))
    print(f'Rango de notas: {min(notas)} - {max(notas)}')

    # ------------------------------------------------------------------
    # 3) DATOS PREPARADOS POR LA COCINA (cruce, cálculo y clasificación)
    # ------------------------------------------------------------------
    datos = preparar_datos(estudiantes, evaluaciones)

    # ------------------------------------------------------------------
    # 4) TABLA COMPLETA (ya viene ordenada por programa y nombre)
    # ------------------------------------------------------------------
    print('\n' + '=' * 70)
    print('2) TABLA COMPLETA (ordenada por programa y nombre)')
    print('=' * 70)
    print(f"{'Identificación':<12}{'Nombre':<27}{'Programa':<29}{'Mód':>4}{'Prom':>7}{'Asist':>7}  Certificado")
    # Ladrillo: BUCLE for que imprime cada fila de la tabla.
    for f in datos['resultados']:
        print(f"{f['identificacion']:<12}{f['nombre']:<27}{f['programa'][:28]:<29}{f['modulos']:>4}"
              f"{f['promedio']:>7.2f}{f['asistencia']:>7.2f}  {f['certificado']}")

    # Resumen de tipos de certificado.
    print('\nResumen por tipo de certificado:')
    print(f"   Aprobación: {datos['contadores']['aprobacion']}")
    print(f"   Participación: {datos['contadores']['participacion']}")
    print(f"   Sin certificado: {datos['contadores']['sin_certificado']}")

    # ------------------------------------------------------------------
    # 5) INCONSISTENCIAS ENTRE AMBOS ARCHIVOS
    # ------------------------------------------------------------------
    print('\n' + '=' * 70)
    print('3) INCONSISTENCIAS')
    print('=' * 70)
    inc = datos['inconsistencias']

    print(f"\na) Estudiantes del maestro SIN ninguna evaluación: {len(inc['sin_evaluaciones'])}")
    for e in inc['sin_evaluaciones']:
        print(f"   {e['identificacion']} — {e['nombre']} ({e['programa']})")

    print(f"\nb) Identificaciones evaluadas que NO están en el maestro: {len(inc['fuera_del_maestro'])}")
    for e in inc['fuera_del_maestro']:
        print(f"   {e['identificacion']} ({e['programa']})")

    print(f"\nc) Grupos con menos de {MAX_MODULOS} módulos: {len(inc['modulos_incompletos'])}")


if __name__ == '__main__':
    preparar_consola()
    # Ladrillo: import de la constante para mostrar el máximo de módulos.
    from modulos.cocina import MAX_MODULOS
    main()
