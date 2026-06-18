@echo off
setlocal

REM Run from the folder that contains this .bat file.
cd /d "%~dp0"

set "VENV_DIR=.venv"
set "REQUIREMENTS_FILE=requirements.txt"

REM Prefer the Windows Python launcher, then fall back to python.
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=py"
) else (
    set "PYTHON_CMD=python"
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
    %PYTHON_CMD% -m venv "%VENV_DIR%"
    if errorlevel 1 goto error
)

"%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto error

"%VENV_DIR%\Scripts\python.exe" -m pip install -r "%REQUIREMENTS_FILE%"
if errorlevel 1 goto error

"%VENV_DIR%\Scripts\python.exe" goodreads_quotes_crawl.py
if errorlevel 1 goto error

goto end

:error
echo.
echo [ERROR] Failed to prepare environment or run crawler.

:end
pause
