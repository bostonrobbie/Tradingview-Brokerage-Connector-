@echo off
title IBKR Bridge Launcher
color 0E

echo ===================================================
echo   Starting IBKR (Interactive Brokers) Bridge
echo ===================================================

echo [1/3] Checking Dependencies...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed.
    pause
    exit
)

echo [2/3] Starting IBKR Bridge Server (Port 5001)...
start "IBKR Bridge" cmd /k "python src/main_ibkr.py"

echo [3/3] Starting Local Tunnel (Port 5001)...
echo.
echo ===================================================
echo   Take note of the URL below! 
echo   Copy it to your TradingView Alert.
echo ===================================================
echo.
:: Start LocalTunnel on Port 5001
cmd /k "lt --port 5001"
