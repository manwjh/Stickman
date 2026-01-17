@echo off
REM Startup script for AI Stick Figure Story Animator (Windows)

echo ============================================
echo 🎬 AI Stick Figure Story Animator
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv venv
    exit /b 1
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if llm_config.yml exists
if not exist "llm_config.yml" (
    echo ⚠️  Warning: llm_config.yml file not found!
    echo Creating from llm_config.example.yml...
    copy llm_config.example.yml llm_config.yml
    echo.
    echo ⚠️  Please edit llm_config.yml and add your API key!
    echo Then run this script again.
    exit /b 1
)

REM Check if requirements are installed
echo 📚 Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

REM Start the application
echo.
echo 🚀 Starting application...
echo.
python app.py
