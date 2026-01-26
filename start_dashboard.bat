@echo off
title IBKR Bridge Dashboard
cd /d "%~dp0"
echo Starting Dashboard...
streamlit run dashboard.py
pause
