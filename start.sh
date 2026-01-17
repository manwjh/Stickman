#!/bin/bash

# Startup script for AI Stick Figure Story Animator

echo "============================================"
echo "🎬 AI Stick Figure Story Animator"
echo "============================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if llm_config.yml exists
if [ ! -f "llm_config.yml" ]; then
    echo "⚠️  Warning: llm_config.yml file not found!"
    echo "Creating from llm_config.example.yml..."
    cp llm_config.example.yml llm_config.yml
    echo ""
    echo "⚠️  Please edit llm_config.yml and add your API key!"
    echo "Then run this script again."
    exit 1
fi

# Check if requirements are installed
echo "📚 Checking dependencies..."
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the application
echo ""
echo "🚀 Starting application..."
echo ""
python app.py
