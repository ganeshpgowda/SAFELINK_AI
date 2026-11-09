# SafeLink AI PowerShell Startup Script
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "     SafeLink AI - Intelligent Fraud URL Detection System" -ForegroundColor Green
Write-Host "     Tagline: Don't click blindly. Check before you trust." -ForegroundColor Yellow
Write-Host "=========================================================================" -ForegroundColor Cyan

$VenvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Host "[ERROR] Virtual environment not found at $VenvPython" -ForegroundColor Red
    exit 1
}

Write-Host "`n[1/2] Starting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Cyan
Start-Process "cmd.exe" -ArgumentList "/k `"$VenvPython`" run_backend.py" -WindowStyle Normal

Start-Sleep -Seconds 2

Write-Host "[2/2] Starting Streamlit Frontend on http://localhost:8501..." -ForegroundColor Cyan
Start-Process "cmd.exe" -ArgumentList "/k `"$VenvPython`" run_frontend.py" -WindowStyle Normal

Write-Host "`nBoth services launched!" -ForegroundColor Green
Write-Host "- Streamlit UI: http://localhost:8501" -ForegroundColor Yellow
Write-Host "- FastAPI Docs: http://127.0.0.1:8000/docs" -ForegroundColor Yellow

