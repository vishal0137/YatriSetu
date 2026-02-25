@echo off
echo ========================================
echo YatriSetu Quick Start
echo ========================================
echo.

echo Choose an option:
echo 1. Start server (no ML)
echo 2. Train ML from database + Start server
echo 3. Run tests
echo 4. Train ML only
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto start_server
if "%choice%"=="2" goto train_and_start
if "%choice%"=="3" goto run_tests
if "%choice%"=="4" goto train_only

:start_server
echo.
echo Starting server...
python run.py
goto end

:train_and_start
echo.
echo Training ML models from database...
python ml/db_trainer.py
if errorlevel 1 (
    echo.
    echo Training failed! Install dependencies:
    echo pip install scikit-learn numpy
    pause
    goto end
)
echo.
echo Starting server...
python run.py
goto end

:run_tests
echo.
echo Running chatbot tests...
python tests/test_chatbot.py
echo.
echo Running ML tests...
python tests/test_ml_models.py
pause
goto end

:train_only
echo.
echo Training ML models from database...
python ml/db_trainer.py
pause
goto end

:end
