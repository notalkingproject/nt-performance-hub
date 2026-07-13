@echo off
setlocal
cd /d "%~dp0"

echo Updating NT Performance Hub from GitHub...
where git >nul 2>nul
if errorlevel 1 (
  echo Git was not found. Install Git for Windows, then run this again.
  pause
  exit /b 1
)

git status --short
if errorlevel 1 goto :error

echo.
echo Pulling latest code...
git pull --ff-only
if errorlevel 1 goto :error

echo.
echo Update complete. Restart NT Performance Hub if it is already running.
pause
exit /b 0

:error
echo.
echo Update failed. Check the message above.
pause
exit /b 1