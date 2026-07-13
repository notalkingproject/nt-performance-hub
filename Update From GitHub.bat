@echo off
setlocal
cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\nt_update_from_github.ps1"
if errorlevel 1 (
  echo.
  echo Update failed. Check the message above.
  pause
  exit /b 1
)

echo.
pause