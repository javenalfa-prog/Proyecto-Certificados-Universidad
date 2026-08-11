# PLAN.md — Academia Horizonte: sistema de certificados

Plan de implementación por etapas. **Seguimos en modo Plan: no se escribe código hasta aprobar cada etapa.**

## Etapa 0 — Entorno (preparar la cocina)

- **Qué hacer**
  - Instalar Python 3 (no está instalado en esta máquina; `python` no existe en PATH).
  - Crear entorno virtual `.venv` y activarlo.
  - Crear `requirements.txt` con las librerías elegidas.
- **Cómo validar**
  - `python --version` responde 3.x.
  - `python -c "import flask, openpyxl"` no da error dentro del venv.

## Etapa 1 — Validación del cruce de datos (bodega)

- **Qué hacer**
  - Escribir `validar.py`: lee ambos Excel con openpyxl y produce un reporte:
    - Encabezados esperados en cada hoja.
    - Conteos: filas del maestro, filas de evaluaciones, grupos (Identificacion + Programa).
    - IDs del maestro sin evaluaciones (esperado: `304560321`).
    - IDs evaluados que no están en el maestro (esperado: `999880777`).
    - Grupos con menos de 4 módulos (esperado: 8, todos de Excel Avanzado con 3).
    - Rangos: notas 0-100, asistencia 0-100, fechas ISO, IDs de 9 dígitos.
  - Decidir política de casos borde (punto de decisión con el usuario):
    - Opción recomendada: certificados solo para estudiantes del maestro con datos; los casos borde aparecen en el reporte, no en la emisión.
- **Cómo validar**
  - El reporte coincide con los números reales medidos en el análisis:
    - Maestro: 24 estudiantes (16 IA, 8 Excel, cohorte 2026-A).
    - Evaluaciones: 88 filas → 24 grupos.
    - 1 ID sin evaluaciones, 1 ID fuera del maestro, 8 grupos con 3/4 módulos, 0 conflictos de programa.

## Etapa 2 — Backend Flask (cocina)

- **Qué hacer**
  - `modulos/bodega.py`: carga los Excel a estructuras de Python (sin modificarlos).
  - `modulos/cocina.py`: funciones puras de negocio:
    - agrupar por Identificacion + Programa;
    - promedio = suma de Notas / módulos cursados;
    - asistencia = promedio de Asistencia_Pct;
    - clasificar: Aprobación (prom >= 70 y asist >= 80), Participación (prom < 70 y asist >= 80), Sin certificado (asist < 80). Límites INCLUSIVOS.
  - `app.py`: servidor Flask con rutas que muestran resultados; sin lógica en el frontend.
- **Cómo validar**
  - Pruebas con casos límite: promedio 70.00 exacto → aprobación; asistencia 80.00 exacta → aprobación; asistencia 79.99 → sin certificado; grupo con 3 módulos promedia sobre 3.
  - Prueba con los Excel reales → los conteos esperados son:
    - Con la política recomendada (solo maestro): **23 estudiantes evaluables** → 19 Aprobación, 3 Participación, 1 Sin certificado, +1 (304560321) sin datos en el reporte.
    - Si se incluye al evaluado fuera del maestro: 20 Aprobación (el extra `999880777`).

## Etapa 3 — Interfaz (salón)

- **Qué hacer**
  - Plantillas Jinja2 en `templates/` servidas por Flask.
  - `static/estilos.css`: diseño azul marino y dorado (Academia Horizonte).
  - Páginas: inicio, reporte de validación, resultados por programa, detalle por estudiante.
  - El HTML solo muestra datos; no calcula ni decide nada (sin JS de cálculo).
- **Cómo validar**
  - Navegador: tablas correctas, tildes y acentos visibles, diseño responsive, sin errores de plantilla.

## Etapa 4 — Prueba integral

- **Qué hacer**
  - Ejecutar la app completa: entorno → validación → backend → interfaz.
  - Revisar flujo completo y documentar comandos de arranque.
- **Cómo validar**
  - Checklist final: arranque con un comando, reporte de validación correcto, conteos 19/3/1 (o 20/3/1 según política), páginas sin errores.

## Estructura de archivos prevista

```
app.py                  # Flask: rutas y servidor
modulos/bodega.py       # lectura de los Excel
modulos/cocina.py       # reglas de negocio
validar.py              # reporte de validación (Etapa 1)
templates/              # páginas HTML (Jinja2)
static/estilos.css      # azul marino y dorado
requirements.txt        # flask, openpyxl, pytest
.venv/                  # entorno virtual (no se versiona)
```
