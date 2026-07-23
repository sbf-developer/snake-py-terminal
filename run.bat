@echo off
cd /d "%~dp0"
python "%~dp0snake.py"
if errorlevel 1 pause
