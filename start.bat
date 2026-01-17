@echo off
REM Startup script for AI Stick Figure Story Animator (Windows)

echo ============================================
echo 🎬 AI Stick Figure Story Animator
echo ============================================
echo.

REM Get port from config.yml (default to 5001)
set PORT=5001
for /f "tokens=2" %%i in ('findstr /C:"port:" config.yml 2^>nul') do set PORT=%%i

REM Check if port is in use and kill the process
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":%PORT%" ^| findstr "LISTENING"') do (
    echo ⚠️  Port %PORT% is already in use
    echo 🔧 Stopping existing process...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
    echo ✅ Port cleared
    echo.
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python 3.9 or higher
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment!
        exit /b 1
    )
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if llm_config.yml exists
if not exist "llm_config.yml" (
    echo ⚠️  Warning: llm_config.yml file not found!
    if exist "llm_config.example.yml" (
        echo Creating from llm_config.example.yml...
        copy llm_config.example.yml llm_config.yml
        echo.
        echo ⚠️  Please edit llm_config.yml and add your API key!
        echo Then run this script again.
        exit /b 1
    ) else (
        echo ❌ llm_config.example.yml not found!
        exit /b 1
    )
)

REM Check if requirements are installed
echo 📚 Checking dependencies...
python -c "import flask, litellm, pyyaml" 2>nul
if errorlevel 1 (
    echo 📦 Installing dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies!
        exit /b 1
    )
    echo ✅ Dependencies installed
)

REM Start the application
echo.
echo 🚀 Starting application...
echo 🌐 Server will be available at: http://127.0.0.1:%PORT%
echo Press Ctrl+C to stop the server
echo.
echo ============================================
echo.
python app.py
