@echo off
setlocal

cd /d "%~dp0"

echo ========================================
echo Daily Rhythm Companion API - Test
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [Error] Virtual environment not found.
    echo Please run run_dev.bat first.
    pause
    exit /b 1
)

echo [Setup] Activating virtual environment...
call ".venv\Scripts\activate.bat"

echo [Test] Running API smoke test...
echo.

powershell -ExecutionPolicy Bypass -File ".\scripts\test_api.ps1"

echo.
echo ========================================
echo Test finished.
echo ========================================
pause