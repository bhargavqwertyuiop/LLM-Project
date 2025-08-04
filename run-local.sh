#!/bin/bash

echo "🚀 Starting DocuMind Local Development Setup"
echo "============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Create virtual environment for Python backend
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies (already done)
echo "📦 Node.js dependencies already installed..."

# Create uploads directory
mkdir -p uploads

# Copy environment file
if [ ! -f .env ]; then
    echo "⚙️ Creating environment file..."
    cp .env.example .env
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Backend API: cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo "2. Frontend: npm start (in a new terminal)"
echo ""
echo "Note: This runs without Ollama/Redis. Some AI features will be limited."
echo "For full functionality, install Docker and use: docker-compose up -d"