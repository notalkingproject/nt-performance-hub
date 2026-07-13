@echo off
setlocal
cd /d "%~dp0"

set "HOST=0.0.0.0"
set "PORT=8080"
if not "%~1"=="" set "PORT=%~1"

set "VENV_PYTHON=%CD%\.venv\Scripts\python.exe"
if exist "%VENV_PYTHON%" (
  set "PYTHON_MODE=venv"
) else (
  where py >nul 2>nul
  if not errorlevel 1 set "PYTHON_MODE=py"
  if not defined PYTHON_MODE (
    where python >nul 2>nul
    if not errorlevel 1 set "PYTHON_MODE=python"
  )
)

if not defined PYTHON_MODE (
  echo Python 3 was not found.
  echo Run Install Portable App.bat first, or install Python 3.11+ and try again.
  pause
  exit /b 1
)

echo Starting NT Performance Hub on http://127.0.0.1:%PORT%/
echo For a tablet, use one of the LAN URLs printed by the server.
echo.

if "%PYTHON_MODE%"=="venv" (
  "%VENV_PYTHON%" app.py --host %HOST% --port %PORT%
) else if "%PYTHON_MODE%"=="py" (
  py -3 app.py --host %HOST% --port %PORT%
) else (
  python app.py --host %HOST% --port %PORT%
)

if errorlevel 1 (
  echo.
  echo The app exited with an error. Check the message above.
  pause
)