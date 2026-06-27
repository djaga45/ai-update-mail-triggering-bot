@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
if not exist logs mkdir logs
start /B pythonw run_scheduler.py