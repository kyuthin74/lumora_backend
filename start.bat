@echo off
REM Lumora Backend - Quick Start Script for Windows

echo ========================================
echo Lumora Mental Health Backend
echo Quick Start Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your settings!
    echo.
    pause
)

REM Start the server
echo Starting Lumora Backend Server...
echo.
echo API will be available at:
echo - http://localhost:8000
echo - Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
