@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
:: update.py writes to update_log.txt internally — do not redirect here
:: (redirecting to the same file causes PermissionError on Windows)
python update.py

:: If Python returned an error code, log it
if %ERRORLEVEL% NEQ 0 (
	echo [%DATE% %TIME%] ERROR: update.py exited with code %ERRORLEVEL% >> update_log.txt
)