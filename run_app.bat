@echo off
echo ============================================
echo   Smart Election Voting System
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirments.txt

REM Initialize database if needed
echo.
echo ============================================
echo   Initializing Database...
echo ============================================
python -c "from app import init_db; init_db()"

REM Run the application
echo.
echo ============================================
echo   Starting Smart Voting Application
echo ============================================
echo   Open your browser and go to:
echo   http://127.0.0.1:5000
echo.
python app.py

pause
