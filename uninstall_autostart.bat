@echo off
cd /d "%~dp0"
echo ============================================
echo  Gmail setup for AI News Email Agent
echo ============================================
echo.
echo Step 1 - Create a Gmail App Password
echo   1. Open https://myaccount.google.com/apppasswords
echo   2. Sign in with the Gmail account that will SEND digests
echo   3. App name: AI News Agent
echo   4. Copy the 16-character password (no spaces)
echo.
echo Step 2 - Enter credentials below
echo.

set /p SMTP_USER=Gmail address (e.g. jagadeesan1914@gmail.com): 
set /p SMTP_PASSWORD=Gmail App Password (16 chars): 

if "%SMTP_USER%"=="" (
  echo Gmail address is required.
  pause
  exit /b 1
)
if "%SMTP_PASSWORD%"=="" (
  echo App password is required.
  pause
  exit /b 1
)

(
echo SMTP_HOST=smtp.gmail.com
echo SMTP_PORT=587
echo SMTP_USER=%SMTP_USER%
echo SMTP_PASSWORD=%SMTP_PASSWORD%
echo FROM_EMAIL=%SMTP_USER%
echo FROM_NAME=AI News Brief
echo DRY_RUN=false
) > .env

echo.
echo .env saved. Testing SMTP connection...
call venv\Scripts\activate.bat
python test_email.py
echo.
pause