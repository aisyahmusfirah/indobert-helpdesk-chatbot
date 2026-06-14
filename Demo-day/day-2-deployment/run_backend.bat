@echo off
cd /d "%~dp0"
..\..\.venv\Scripts\uvicorn main:app --port 8000