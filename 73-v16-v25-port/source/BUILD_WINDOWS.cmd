@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  python build_apk.py
) else (
  py -3 build_apk.py
)
pause
