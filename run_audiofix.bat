@echo off
REM run_audiofix.bat
REM Starts audiofix.py using the project's virtual environment in the background.
REM Prefers pythonw.exe (no console). Falls back to python.exe started minimized.

SETLOCAL

REM Directory containing this batch file (ends with a backslash)
SET "SCRIPT_DIR=%~dp0"

REM Paths to virtualenv python executables (adjust if your venv has a different name)
SET "PYTHONW=%SCRIPT_DIR%\.venv\Scripts\pythonw.exe"
SET "PYTHON=%SCRIPT_DIR%\.venv\Scripts\python.exe"
SET "SCRIPT=%SCRIPT_DIR%audiofix.py"

IF EXIST "%PYTHONW%" (
    REM Launch with pythonw (no console window)
    START "" /D "%SCRIPT_DIR%" "%PYTHONW%" "%SCRIPT%"
) ELSE IF EXIST "%PYTHON%" (
    REM Launch python in a new minimized window (best-effort background)
    START "" /MIN /D "%SCRIPT_DIR%" "%PYTHON%" "%SCRIPT%"
) ELSE (
    ECHO Could not find a Python executable in "%SCRIPT_DIR%\.venv\Scripts".
    ECHO Please create the virtualenv at "%SCRIPT_DIR%\.venv" or edit this batch file to point to a Python install.
    PAUSE
)

ENDLOCAL
