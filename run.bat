@echo off
REM Verifica si Python está instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python no está instalado o no está en el PATH.
    pause
    exit /b
)

REM Ejecuta el script main.py
echo Ejecutando main.py...
python "%~dp0main.py"

REM Espera antes de cerrar la ventana
echo Presiona una tecla para salir.
pause