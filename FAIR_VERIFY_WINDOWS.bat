@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher not installed. Install 64-bit Python 3.12.
  pause
  exit /b 1
)
py -3.12 -c "import struct,sys; assert sys.version_info[:2]==(3,12) and struct.calcsize('P')*8==64" >nul 2>&1
if errorlevel 1 (
  echo This audit requires 64-bit Python 3.12.
  pause
  exit /b 1
)
if not exist ".venv_FAIR_AUDIT\Scripts\python.exe" py -3.12 -m venv ".venv_FAIR_AUDIT"
if errorlevel 1 goto :FAILED
".venv_FAIR_AUDIT\Scripts\python.exe" -m pip install --only-binary=:all: numpy==1.26.4 pandas==2.2.3
if errorlevel 1 goto :FAILED
".venv_FAIR_AUDIT\Scripts\python.exe" FAIR_VERIFY.py --verify
if errorlevel 1 goto :FAILED
echo.
echo ALL 56 FaIR CASES and 152 SUPPLEMENTARY COMPARISONS VERIFIED.
pause
exit /b 0
:FAILED
echo Audit did not complete. Please preserve this console output.
pause
exit /b 1
