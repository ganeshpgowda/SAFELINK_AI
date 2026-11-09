@echo off
echo =========================================================================
echo      SafeLink AI - Intelligent Fraud URL Detection System
echo      Tagline: Don't click blindly. Check before you trust.
echo =========================================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Please run: py -m venv .venv
    pause
    exit /b 1
)

echo [1/2] Starting SafeLink AI FastAPI Backend on http://127.0.0.1:8000...
start "SafeLink AI - Backend API" cmd /k ".venv\Scripts\python.exe run_backend.py"

echo [2/2] Starting SafeLink AI Streamlit Frontend on http://localhost:8501...
start "SafeLink AI - Web UI" cmd /k ".venv\Scripts\python.exe run_frontend.py"

echo.
echo SafeLink AI is now running!
echo - Web Dashboard: http://localhost:8501
echo - API Docs:      http://127.0.0.1:8000/docs
echo =========================================================================
pause

