@echo off
REM ============================================================
REM iniciar_app.bat — Academia Horizonte: arranca la app web
REM Doble clic para iniciar. La página se abre en el navegador.
REM Para detenerla: cerrar esta ventana o Ctrl+C.
REM ============================================================

REM Ladrillo: ir a la carpeta del proyecto (donde vive este archivo).
cd /d "%~dp0"

REM Ladrillo: activar el entorno virtual para usar Flask y openpyxl.
call .venv\Scripts\activate.bat

REM Ladrillo: abrir el navegador en la página (2 segundos para que arranque).
start "" /min cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:5000"

REM Ladrillo: arrancar el servidor Flask (este comando NO se cierra solo).
python app.py

REM Ladrillo: si el servidor se detiene, la ventana queda abierta para ver el error.
pause