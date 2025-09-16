@echo off
REM Activar el entorno virtual
call venv\Scripts\activate

REM Ejecutar el servidor de desarrollo
python manage.py runserver

REM Mantener la ventana abierta si hay error
pause
REM Desactivar el entorno virtual al cerrar el servidor
deactivate