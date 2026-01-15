@echo off
title IBKR Diagnostics
cd /d "%~dp0"
python src/qa_diagnostics.py
pause
