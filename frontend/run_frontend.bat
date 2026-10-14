@echo off
title DarkPattern Sentinel - Frontend (React Vite)
color 0B
cd /d "%~dp0"

echo =====================================================================
echo  DarkPattern Sentinel - React/Vite Frontend Dashboard
echo =====================================================================
echo.

if exist "C:\Program Files\nodejs\npm.cmd" (
    set "PATH=C:\Program Files\nodejs;%PATH%"
    set "NPM_CMD=C:\Program Files\nodejs\npm.cmd"
) else if exist "%NODE_DIR%\node.exe" (
    set "PATH=%NODE_DIR%;%PATH%"
    set "NPM_CMD=%NODE_DIR%\npm.cmd"
) else (
    set "NPM_CMD=npm"
)

echo Package Manager: "%NPM_CMD%"
echo Starting Vite Dev Server at http://localhost:5173 ...
echo.

call "%NPM_CMD%" run dev
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Frontend server stopped with an error code %ERRORLEVEL%.
    pause
)
