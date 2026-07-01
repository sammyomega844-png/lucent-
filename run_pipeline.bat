@echo off
setlocal
cd /d "%~dp0"

echo [pipeline] Step 1/3: Running backend update...
call run_update.bat
if %ERRORLEVEL% NEQ 0 (
  echo [pipeline] ERROR: Backend update failed with code %ERRORLEVEL%.
  exit /b %ERRORLEVEL%
)

echo [pipeline] Step 2/3: Syncing frontend artifacts...
call npm.cmd --prefix frontend-lovable run sync:data
if %ERRORLEVEL% NEQ 0 (
  echo [pipeline] ERROR: Artifact sync failed with code %ERRORLEVEL%.
  exit /b %ERRORLEVEL%
)

echo [pipeline] Step 3/3: Building frontend...
call npm.cmd --prefix frontend-lovable run build
if %ERRORLEVEL% NEQ 0 (
  echo [pipeline] ERROR: Frontend build failed with code %ERRORLEVEL%.
  exit /b %ERRORLEVEL%
)

echo [pipeline] SUCCESS: Backend update, data sync, and frontend build completed.
exit /b 0
