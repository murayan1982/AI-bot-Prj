@echo off
setlocal

cd /d "%~dp0"

echo ========================================
echo Daily Rhythm Companion API - Dev Server
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [Setup] Virtual environment not found.
    echo [Setup] Creating .venv...
    python -m venv .venv
    if errorlevel 1 (
        echo [Error] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo [Setup] Activating virtual environment...
call ".venv\Scripts\activate.bat"

echo [Setup] Checking dependencies...
python -m pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [Setup] Installing dependencies...
    python -m pip install fastapi uvicorn
    if errorlevel 1 (
        echo [Error] Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo.
echo [Start] Starting FastAPI dev server...
echo [URL]   http://127.0.0.1:8000
echo [Docs]  http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop.
echo.

python -m uvicorn app.main:app --reload

echo.
echo [Stopped] FastAPI server stopped.
pause