# -*- coding: utf-8 -*-
"""
app.py — Servidor web de Academia Horizonte (Flask).

La cocina (modulos/) prepara los datos y el salón (templates/) solo los
muestra. Aquí solo se definen las rutas del servidor y el filtro.

Arranque:  python app.py   (o doble clic en iniciar_app.bat)
Página:    http://localhost:5000
"""

from flask import Flask, render_template, request

# Ladrillo: importar la Bodega (lectura) y la Cocina (reglas de negocio).
from modulos.bodega import cargar_estudiantes, cargar_evaluaciones
from modulos.cocina import preparar_datos

# Ladrillo: VARIABLE con la aplicación Flask (el servidor web).
app = Flask(__name__)


# Ladrillo: FUNCIÓN de la ruta principal (decorador @app.route).
@app.route('/')
def index():
    """Página principal: contadores, tabla con filtro e inconsistencias.

    TIPO de retorno: HTML renderizado por la plantilla Jinja2.
    """
    # Ladrillo: VARIABLES con los datos crudos, leídos de la Bodega.
    estudiantes = cargar_estudiantes()
    evaluaciones = cargar_evaluaciones()

    # Ladrillo: llamada a la FUNCIÓN de la cocina que cruza y calcula.
    datos = preparar_datos(estudiantes, evaluaciones)

    # Ladrillo: VARIABLE con el filtro de programa elegido en el formulario.
    programa = request.args.get('programa', '').strip()

    # Ladrillo: CONDICIONAL para aplicar el filtro sobre la tabla.
    if programa:
        # Ladrillo: BUCLE con CONDICIONAL (comprensión de listas) para filtrar.
        filas = [f for f in datos['resultados'] if f['programa'] == programa]
    else:
        filas = datos['resultados']

    # Ladrillo: renderiza la plantilla pasándole las VARIABLES de la página.
    return render_template(
        'index.html',
        filas=filas,
        programas=datos['programas'],
        programa_seleccionado=programa,
        contadores=datos['contadores'],
        inconsistencias=datos['inconsistencias'],
        total_mostrados=len(filas),
        total_general=len(datos['resultados']),
    )


if __name__ == '__main__':
    # Ladrillo: arranque del servidor en localhost:5000 (modo desarrollo).
    app.run(host='127.0.0.1', port=5000, debug=True)
