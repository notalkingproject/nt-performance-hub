@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python 3 was not found. Install Python 3.11+ from python.org, then run this again.
    pause
    exit /b 1
  )
  set "PYTHON_CMD=python"
) else (
  set "PYTHON_CMD=py -3"
)

echo Creating local virtual environment in .venv ...
%PYTHON_CMD% -m venv .venv
if errorlevel 1 goto :error

echo Installing Python dependencies ...
"%CD%\.venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
"%CD%\.venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Install complete. Start the app with Start NT Performance Hub.bat.
pause
exit /b 0

:error
echo.
echo Install failed. Check the message above.
pause
exit /b 1