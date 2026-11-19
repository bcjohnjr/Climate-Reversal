@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3.12 APPLY_REPOSITORY_CLEANUP.py
) else (
  python APPLY_REPOSITORY_CLEANUP.py
)
echo.
echo Check errors and the GitHub repository before journal submission.
pause
