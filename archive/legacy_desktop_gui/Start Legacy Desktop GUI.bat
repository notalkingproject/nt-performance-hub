@echo off
setlocal

cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 "%~dp0launcher.py"
    goto :done
)

where python >nul 2>nul
if %errorlevel%==0 (
    python "%~dp0launcher.py"
    goto :done
)

start "" "%~dp0launcher.py"

:done
