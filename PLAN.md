# PLAN.md — Academia Horizonte: sistema de certificados

Plan de implementación por etapas. **Estado: COMPLETADO.** Todas las etapas
fueron implementadas y verificadas con los datos reales de `Insumos/`.

## Etapa 0 — Entorno ✅

- **Qué hacer**
  - Instalar Python 3.
  - Crear entorno virtual `.venv` y activarlo.
  - Crear `requirements.txt` con `flask`, `openpyxl`, `pytest`.
- **Cómo validar**
  - `python --version` responde 3.x. ✅
  - `python -c "import flask, openpyxl"` no da error dentro del venv. ✅

## Etapa 1 — Validación del cruce de datos (bodega) ✅

- **Qué hacer**
  - `validar.py`: lee ambos Excel con openpyxl y produce un reporte (resumen
    general, tabla completa por estudiante+programa e inconsistencias).
  - Política de casos borde acordada: certificados solo para estudiantes del
    maestro con datos; los casos borde solo aparecen en el reporte.
- **Cómo validar**
  - Reporte coincide con los números reales:
    - Maestro: 24 estudiantes (16 IA, 8 Excel, cohorte 2026-A). ✅
    - Evaluaciones: 88 filas → 24 grupos. ✅
    - 1 ID sin evaluaciones (`304560321`), 1 fuera del maestro (`999880777`),
      8 grupos con módulos incompletos. ✅

## Etapa 2 — Backend Flask (cocina) ✅

- **Qué hacer**
  - `modulos/bodega.py`: carga los Excel a estructuras de Python (sin modificarlos).
  - `modulos/cocina.py`: funciones puras de negocio: agrupar por Identificacion +
    Programa; promedio = suma de Notas / módulos cursados; asistencia = promedio
    de Asistencia_Pct; clasificar Aprobación/Participación/Sin certificado con
    límites INCLUSIVOS.
  - `app.py`: servidor Flask con rutas que muestran resultados; sin lógica en el frontend.
- **Cómo validar**
  - Pruebas de caso límite (70.00 exacto → aprobación; 80.00 → aprobación;
    79.99 → sin certificado; grupo de 3 módulos promedia sobre 3). ✅
  - Prueba con los Excel reales → **19 Aprobación, 3 Participación, 1 Sin
    certificado** (el evaluado fuera del maestro `999880777` no cuenta). ✅
  - Camila Rojas (101230456): promedio 91.25, asistencia 96.25, Aprobación. ✅

## Etapa 3 — Interfaz (salón) ✅

- **Qué hacer**
  - Plantillas Jinja2 en `templates/index.html` servidas por Flask.
  - `static/estilos.css`: diseño azul marino y dorado (Academia Horizonte).
  - Filtro por programa. El HTML solo muestra datos; no calcula ni decide. ✅
- **Cómo validar**
  - Navegador: contadores 19/3/1, filas con color (verde/azul/rojo),
    tildes visibles, sección de inconsistencias. ✅

## Etapa 4 — Prueba integral ✅

- **Qué hacer**
  - Ejecutar la app completa de punta a punta.
- **Cómo validar**
  - `pytest`: **15/15 aprobadas**. ✅
  - Página principal `http://localhost:5000`: HTTP 200, contadores e
    inconsistencias correctas. ✅
  - Arranque con doble clic: `iniciar_app.bat` (abre el navegador). ✅

## Estructura de archivos final

```
app.py                  # Flask: rutas y servidor
modulos/bodega.py       # lectura de los Excel
modulos/cocina.py       # reglas de negocio
validar.py              # reporte de validación por consola
templates/index.html    # página web (Jinja2)
static/estilos.css      # azul marino y dorado
tests/                  # 15 pruebas pytest
Insumos/                # Excel de entrada (no versionado)
requirements.txt        # flask, openpyxl, pytest
iniciar_app.bat         # arranque con doble clic
AGENTS.md               # contexto y reglas del proyecto
.venv/                  # entorno virtual (no versionado)
```

## Repositorio

Proyecto versionado en GitHub: `javenalfa-prog/Proyecto-Certificados-Universidad`.
`Insumos/` y `.venv/` se excluyen con `.gitignore` (los datos no se versionan).