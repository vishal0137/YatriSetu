@echo off
echo ============================================================
echo Restarting YatriSetu Server
echo ============================================================
echo.

echo Stopping any running Flask servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq YatriSetu*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Flask server with updated configuration...
echo.
echo Server will start at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

python run.py

pause
