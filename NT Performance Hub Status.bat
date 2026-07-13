@echo off
setlocal
cd /d "%~dp0"

set "PORT=8080"
if not "%~1"=="" set "PORT=%~1"

set "VENV_PYTHON=%CD%\.venv\Scripts\python.exe"
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" tools\nt_server_action.py status --port %PORT%
) else (
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 tools\nt_server_action.py status --port %PORT%
  ) else (
    where python >nul 2>nul
    if errorlevel 1 (
      echo Python 3 was not found.
      pause
      exit /b 1
    )
    python tools\nt_server_action.py status --port %PORT%
  )
)

pause
