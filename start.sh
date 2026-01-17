#!/bin/bash

# Startup script for AI Stick Figure Story Animator

echo "============================================"
echo "🎬 AI Stick Figure Story Animator"
echo "============================================"
echo ""

# Get port from config.yml (default to 5001)
PORT=$(grep -A 3 "^server:" config.yml 2>/dev/null | grep "port:" | awk '{print $2}' | tr -d ' ')
PORT=${PORT:-5001}

# Check if port is in use and kill the process
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port $PORT is already in use"
    PIDS=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
    PROCESS_NAME=$(ps -p $PIDS -o comm= 2>/dev/null | head -1)
    echo "🔧 Stopping existing process (PID: $PIDS, Process: $PROCESS_NAME)..."
    for PID in $PIDS; do
        kill $PID 2>/dev/null
    done
    sleep 2
    # Verify port is cleared
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "❌ Failed to clear port $PORT"
        exit 1
    fi
    echo "✅ Port cleared"
    echo ""
fi

# Check Python version
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    if [[ "$PYTHON_VERSION" == 3.* ]]; then
        PYTHON_CMD="python"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Python 3 not found!"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment!"
        exit 1
    fi
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment!"
    exit 1
fi

# Check if llm_config.yml exists
if [ ! -f "llm_config.yml" ]; then
    echo "⚠️  Warning: llm_config.yml file not found!"
    if [ -f "llm_config.example.yml" ]; then
        echo "Creating from llm_config.example.yml..."
        cp llm_config.example.yml llm_config.yml
        echo ""
        echo "⚠️  Please edit llm_config.yml and add your API key!"
        echo "Then run this script again."
        exit 1
    else
        echo "❌ llm_config.example.yml not found!"
        exit 1
    fi
fi

# Check if requirements are installed
echo "📚 Checking dependencies..."
python -c "import flask, flask_cors, dotenv, yaml, litellm, pydantic, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies!"
        exit 1
    fi
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies installed"
fi

# Start the application
echo ""
echo "🚀 Starting application..."
echo "🌐 Server will be available at: http://127.0.0.1:$PORT"
echo "Press Ctrl+C to stop the server"
echo ""
echo "============================================"
echo ""
python app.py
