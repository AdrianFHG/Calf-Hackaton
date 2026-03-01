@echo off
title Merchant Dashboard Runner
echo ====================================================
echo   INSTALLING REQUIREMENTS & STARTING SERVICES
echo ====================================================

:: 1. Install Requirements (Mencari file di root atau Backend)
echo [1/3] Checking dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
)

:: 2. Jalankan Backend (FastAPI)
:: Menggunakan 'python -m uvicorn' agar lebih stabil di Windows
echo [2/3] Starting Backend Server...
start "Backend (FastAPI)" cmd /k "cd Backend && python -m uvicorn backend:app --host 127.0.0.1 --port 8000"

:: 3. Jalankan Frontend (Streamlit)
echo [3/3] Starting Frontend Dashboard...
start "Frontend (Streamlit)" cmd /k "cd Frontend && python -m streamlit run app.py"

echo ====================================================
echo   SUCCESS: Dashboard is being launched!
echo ====================================================
pause