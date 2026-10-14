@echo off
title DarkPattern Sentinel System Launcher
color 0B

echo =====================================================================
echo  AI-DRIVEN DARK PATTERN DETECTION AND CCPA COMPLIANCE SENTINEL
echo  7th Semester Major Engineering Project Launcher
echo =====================================================================
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo [1/3] Starting FastAPI Backend Server on port 8000 ...
start "DarkPattern Sentinel - Backend" "%PROJECT_DIR%backend\run_backend.bat"

REM Allow backend to initialize database
timeout /t 2 /nobreak >nul

echo [2/3] Starting React Vite Frontend Dashboard on port 5173 ...
start "DarkPattern Sentinel - Frontend" "%PROJECT_DIR%frontend\run_frontend.bat"

echo.
echo [3/3] Opening Web Browser to http://localhost:5173 ...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo =====================================================================
echo  Both services launched successfully!
echo  - Frontend Dashboard: http://localhost:5173
echo  - Backend API:        http://127.0.0.1:8000
echo  - Interactive Docs:   http://127.0.0.1:8000/docs
echo =====================================================================
echo.
echo Note: Keep the two service console windows open while testing.
timeout /t 5 >nul
