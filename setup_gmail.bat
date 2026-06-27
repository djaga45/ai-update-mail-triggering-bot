@echo off
cd /d "%~dp0"
py -3.13 -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
streamlit run app.py