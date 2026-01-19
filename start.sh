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

# Detect Python command (prioritize venv Python if available)
PYTHON_CMD=""
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "❌ Python not found!"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

# Check if we're already in a virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "🐍 Using Python from venv: $VIRTUAL_ENV"
else
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
    
    # Update PYTHON_CMD to use venv python
    PYTHON_CMD="python"
fi

# Check if API keys are set in environment variables
echo "🔑 Checking API keys in environment..."
PROVIDER=$(grep -A 3 "^llm:" config.yml 2>/dev/null | grep "provider:" | awk '{print $2}' | tr -d ' ')
PROVIDER=${PROVIDER:-openai}

API_KEY_SET=false
case "$PROVIDER" in
    openai)
        [ ! -z "$OPENAI_API_KEY" ] && API_KEY_SET=true
        ;;
    anthropic)
        [ ! -z "$ANTHROPIC_API_KEY" ] && API_KEY_SET=true
        ;;
    perfxcloud)
        [ ! -z "$PERFXCLOUD_API_KEY" ] && API_KEY_SET=true
        ;;
esac

if [ "$API_KEY_SET" = false ]; then
    echo "❌ API key for provider '$PROVIDER' not found in environment!"
    echo ""
    echo "Please set API keys first:"
    echo "  $ source ./set_env.sh"
    echo ""
    echo "Then run this script again:"
    echo "  $ ./start.sh"
    echo ""
    exit 1
fi
echo "✅ API key found for provider: $PROVIDER"
echo ""

# Check if requirements are installed
echo "📚 Checking dependencies..."
$PYTHON_CMD -c "import flask, flask_cors, dotenv, yaml, litellm, pydantic, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    $PYTHON_CMD -m pip install --upgrade pip
    $PYTHON_CMD -m pip install -r requirements.txt
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

# 设置Cairo库路径（macOS需要）
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/cairo/lib:$DYLD_LIBRARY_PATH"

$PYTHON_CMD app.py
