@echo off
REM YatriSetu Production Startup Script
REM This script starts the YatriSetu server in production mode

echo ======================================================================
echo YatriSetu - Smart Transit Platform
echo Production Server Startup
echo ======================================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run scripts\setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Using default configuration...
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Clear old logs (optional)
echo Clearing old logs...
if exist "logs\app.log" del /q "logs\app.log"

REM Check database connection
echo Checking database connection...
python -c "from app import create_app; app = create_app(); print('Database connection: OK')" 2>nul
if errorlevel 1 (
    echo WARNING: Database connection failed!
    echo Server will start but database features may not work
)

REM Start the server
echo.
echo Starting YatriSetu server...
echo.
python run.py

REM If server stops
echo.
echo Server stopped.
pause
