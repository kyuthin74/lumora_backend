#!/bin/bash
# Lumora Backend - Quick Start Script for Linux/Mac

echo "========================================"
echo "Lumora Mental Health Backend"
echo "Quick Start Script"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env file with your settings!"
    echo ""
    read -p "Press enter to continue..."
fi

# Start the server
echo "Starting Lumora Backend Server..."
echo ""
echo "API will be available at:"
echo "- http://localhost:8000"
echo "- Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
