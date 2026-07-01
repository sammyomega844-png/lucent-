@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
:: briefing.py writes to briefing_log.txt internally — do not redirect here
:: (redirecting to the same file causes PermissionError on Windows)
python briefing.py
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%
