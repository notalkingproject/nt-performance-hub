@echo off
setlocal
cd /d "%~dp0"

set "PORT=8080"
if not "%~1"=="" set "PORT=%~1"

set "VENV_PYTHON=%CD%\.venv\Scripts\python.exe"
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" tools\nt_server_action.py restart --port %PORT% --open
) else (
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 tools\nt_server_action.py restart --port %PORT% --open
  ) else (
    where python >nul 2>nul
    if errorlevel 1 (
      echo Python 3 was not found.
      echo Run Install NT Performance Hub.bat first, or install Python 3.11+ and try again.
      pause
      exit /b 1
    )
    python tools\nt_server_action.py restart --port %PORT% --open
  )
)

if errorlevel 1 (
  echo.
  echo Restart failed. Check the message above.
  pause
  exit /b 1
)

echo.
echo NT Performance Hub restarted.
pause
