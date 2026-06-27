@echo off
cd /d "%~dp0"
set TASK_NAME=AI News Email Agent
set RUN_CMD=%~dp0run_background.bat

schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1
schtasks /Create /TN "%TASK_NAME%" /TR "\"%RUN_CMD%\"" /SC ONLOGON /RL LIMITED /F
if errorlevel 1 (
  echo Failed to create scheduled task. Try running this file as Administrator.
  pause
  exit /b 1
)

echo.
echo Auto-start installed successfully.
echo Task name: %TASK_NAME%
echo Runs at:   Every Windows logon
echo Command:   %RUN_CMD%
echo Logs:      %~dp0logs\scheduler.log
echo.
echo To remove later, run uninstall_autostart.bat
pause