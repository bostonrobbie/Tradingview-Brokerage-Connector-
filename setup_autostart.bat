@echo off
set "SCRIPT_PATH=%~dp0start_ibkr.bat"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\TV_IBKR_Bridge.lnk"

echo Setting up Auto-Start for: %SCRIPT_PATH%

powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%');$s.TargetPath='%SCRIPT_PATH%';$s.Save()"

echo.
echo ========================================================
echo SUCCESS! The IBKR Bridge will now start automatically.
echo ========================================================
pause
