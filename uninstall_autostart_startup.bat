@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
streamlit run app.py