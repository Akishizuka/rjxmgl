@echo off
chcp 65001 >nul
cd /d "%~dp0"
call .\venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
pause
