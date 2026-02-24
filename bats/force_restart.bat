@echo off
echo ============================================================
echo Force Restart YatriSetu Server
echo ============================================================
echo.

echo Stopping ALL Python processes...
taskkill /F /IM python.exe 2>nul
if %errorlevel% equ 0 (
    echo Python processes stopped.
) else (
    echo No Python processes were running.
)

echo.
echo Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo ============================================================
echo Starting Fresh Flask Server
echo ============================================================
echo.
echo Database: yatrisetu_db
echo Password: Vi21@189 (from .env)
echo.
echo Server will start at: http://localhost:5000
echo.
echo Once you see "Running on http://127.0.0.1:5000"
echo Open your browser and refresh the page.
echo.
echo Press Ctrl+C to stop the server when done.
echo ============================================================
echo.

python run.py

pause
