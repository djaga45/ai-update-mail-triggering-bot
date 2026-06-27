@echo off
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set LINK=%STARTUP%\AI News Email Agent.bat

(
echo @echo off
echo cd /d "%%~dp0"
echo start "" /B "%%~dp0run_background.bat"
) > "%LINK%"

echo Auto-start added to Windows Startup folder:
echo %LINK%
echo.
echo The scheduler will start silently each time you log in.
echo To remove: delete that file from Startup, or run uninstall_autostart_startup.bat
pause