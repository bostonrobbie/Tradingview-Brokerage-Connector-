@echo off
title One-Click GitHub Backup
color 0A
cd /d "%~dp0"

echo ===================================================
echo   Backing up IBKR Bridge to GitHub
echo ===================================================

echo [1/3] Adding all files...
git add .

echo [2/3] Committing changes...
set "TIMESTAMP=%date% %time%"
git commit -m "Auto-Backup: %TIMESTAMP%"

echo [3/3] Pushing to GitHub...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Your code is safe on GitHub!
) else (
    echo.
    echo [ERROR] Something went wrong.
)
pause
