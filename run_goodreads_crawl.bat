@echo off
setlocal

REM Run from the folder that contains this .bat file.
cd /d "%~dp0"

REM Prefer the Windows Python launcher, then fall back to python.
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py goodreads_quotes_crawl.py
) else (
    python goodreads_quotes_crawl.py
)

pause
