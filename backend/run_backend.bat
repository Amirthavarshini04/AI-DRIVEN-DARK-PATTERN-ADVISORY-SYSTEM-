@echo off
title DarkPattern Sentinel - Backend (FastAPI)
color 0A
cd /d "%~dp0"

echo =====================================================================
echo  DarkPattern Sentinel - FastAPI Backend Server
echo =====================================================================
echo.

set "PY_CMD="
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0.venv\Scripts\python.exe"
) else if exist "C:\Users\Amirtha S\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PY_CMD=C:\Users\Amirtha S\AppData\Local\Programs\Python\Python312\python.exe"
) else if exist "C:\Users\Amirtha S\AppData\Local\Programs\Python\Python310\python.exe" (
    set "PY_CMD=C:\Users\Amirtha S\AppData\Local\Programs\Python\Python310\python.exe"
) else (
    set "PY_CMD=python"
)

echo Python Interpreter: "%PY_CMD%"
echo Starting FastAPI Server at http://127.0.0.1:8000 ...
echo.

"%PY_CMD%" main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Backend server stopped with an error code %ERRORLEVEL%.
    pause
)
