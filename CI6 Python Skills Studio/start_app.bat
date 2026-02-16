@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv" (
  py -3 -m venv .venv 2>nul
  if errorlevel 1 (
    python -m venv .venv
  )
)

call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt

start "" http://127.0.0.1:5050
python app.py

endlocal
