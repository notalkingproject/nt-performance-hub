@echo off
setlocal
cd /d "%~dp0"

echo NT Performance Hub - Push To GitHub
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo Git was not found. Install Git for Windows, then run this again.
  pause
  exit /b 1
)

git status --short
if errorlevel 1 goto :error

echo.
set "COMMIT_MESSAGE="
set /p COMMIT_MESSAGE="Update note for this push: "
if "%COMMIT_MESSAGE%"=="" set "COMMIT_MESSAGE=Update NT Performance Hub"

echo.
echo Staging changes...
git add -A
if errorlevel 1 goto :error

git diff --cached --quiet
if not errorlevel 1 goto :no_changes

echo.
echo Committing: %COMMIT_MESSAGE%
git commit -m "%COMMIT_MESSAGE%"
if errorlevel 1 goto :error

goto :push

:no_changes
echo.
echo No local file changes to commit.

:push
echo.
echo Pushing to GitHub...
git push
if errorlevel 1 goto :error

echo.
echo Push complete.
pause
exit /b 0

:error
echo.
echo Push failed. Check the message above.
pause
exit /b 1