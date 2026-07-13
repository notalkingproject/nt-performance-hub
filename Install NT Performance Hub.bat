@echo off
setlocal
cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\nt_install.ps1"
if errorlevel 1 (
  echo.
  echo Install failed. Check the message above.
  pause
  exit /b 1
)

echo.
pause