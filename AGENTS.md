# AGENTS.md

## Idioma

- El usuario escribe en español. Responde siempre en español (mantén el código, identificadores y contenidos de archivos en su idioma original).

## Contexto del proyecto

Somos Academia Horizonte, un centro de formación que imparte programas técnicos a empresas. Al cerrar cada cohorte emitimos certificados por estudiante. Hoy el proceso es manual en Excel y Word; vamos a automatizarlo como una APLICACIÓN WEB.

## Arquitectura (3 piezas)

- Bodega (datos): los Excel en `Insumos/`. NO se modifican.
- Cocina (backend): Python con Flask, en `app.py`. Toda la lógica va aquí, NUNCA en la interfaz.
- Salón (frontend): páginas web HTML servidas por Flask. Solo muestra información; no calcula ni decide.

## Archivos de entrada

Ambos son `.xlsx` (zip+XML; no hay exportaciones CSV). Están en `Insumos/`.

- `Insumos/Maestro_Estudiantes.xlsx` — hoja `Estudiantes`, lista oficial de 24 estudiantes. Columnas: `Identificacion` (9 dígitos), `Nombre_Completo`, `Correo`, `Programa`, `Cohorte` (ej. `2026-A`).
- `Insumos/Registro_Evaluaciones.xlsx` — hoja `Evaluaciones`, 88 filas, notas (0-100) y asistencia por módulo. Columnas: `Identificacion`, `Programa`, `Modulo` (`Módulo 1`..`4`), `Nota`, `Asistencia_Pct`, `Fecha_Cierre` (fechas ISO, 2026). Cada estudiante tiene hasta 4 filas.

## Reglas de negocio

IMPORTANTE: Promedio = suma de Notas / cantidad de módulos cursados.
Asistencia = promedio de `Asistencia_Pct`.
IMPORTANTE: Se agrupa por Identificacion + Programa. Un certificado por estudiante y programa.
IMPORTANTE: Aprobación si Promedio >= 70 y Asistencia >= 80.
Participación si Promedio < 70 y Asistencia >= 80.
Sin certificado si Asistencia < 80. Los límites INCLUYEN el valor.

## Gotchas

- Ambos archivos congelan la fila 1 (encabezados); los datos empiezan en la fila 2. Léelos como XLSX, no como texto.
- Los datos son inconsistentes entre archivos: `304560321` está en el maestro pero no tiene evaluaciones; `999880777` tiene evaluaciones pero no está en el maestro (ID de prueba). Nunca asumas que todo estudiante tiene los 4 módulos ni que todo evaluado existe en el maestro.
- El texto en español con acentos (ej. `Técnico en IA Aplicada`) es UTF-8 válido; no lo recodifiques.
- Programas en uso: `Técnico en IA Aplicada` y `Excel Avanzado para Negocios`.

## Estilo de trabajo

- Código simple y comentado en español, señalando dónde están los ladrillos: variables, tipos, condicionales, bucles y funciones.
- Diseño web en azul marino y dorado.
- Explícame en español sencillo lo que vayas haciendo.
