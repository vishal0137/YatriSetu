@echo off
echo ============================================================
echo            YatriSetu - Starting Server
echo ============================================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Flask server...
echo.
echo Server will be available at:
echo   - http://localhost:5000 (Home)
echo   - http://localhost:5000/admin (Admin Dashboard with Chatbot)
echo   - http://localhost:5000/chatbot (Standalone Chatbot)
echo.
echo Press CTRL+C to stop the server
echo ============================================================
echo.

python run.py
