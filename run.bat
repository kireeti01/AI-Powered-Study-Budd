@echo off
REM AI Study Buddy - Run Script for Windows
REM This script activates the virtual environment and runs Streamlit

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   AI Study Buddy - Application Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found.
    echo Please run: python setup.py
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo Warning: .env file not found.
    echo Please configure your API key in .env file
    echo.
)

REM Run Streamlit
echo Starting AI Study Buddy...
echo.
echo Note: Press Ctrl+C to stop the application
echo.

streamlit run app.py

pause
