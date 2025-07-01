#!/bin/bash

# Meta Content Manager Launcher Script

echo "🚀 Meta Content Manager"
echo "======================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "web_app.py" ]; then
    echo "❌ Please run this script from the project directory"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Please edit .env file with your Meta app credentials"
    echo ""
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
python3 -c "import flask, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing dependencies..."
    python3 -m pip install -r requirements.txt
fi

echo ""
echo "🌐 Starting Meta Content Manager Web Interface..."
echo "📱 Open your browser to: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop"
echo ""

# Start the web application
python3 start_web.py