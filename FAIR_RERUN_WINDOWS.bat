@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Requires Python Launcher with Python 3.12.
  pause
  exit /b 1
)
py -3.12 FAIR_VERIFY.py --extract-code --workspace "FAIR_RERUN_WORKSPACE"
if errorlevel 1 (
  echo Could not extract reproducibility sources; avoid reusing an existing work directory.
  pause
  exit /b 1
)
cd FAIR_RERUN_WORKSPACE
call RUN_FULL_WINDOWS.bat
exit /b %errorlevel%
