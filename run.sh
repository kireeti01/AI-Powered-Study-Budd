#!/bin/bash
# AI Study Buddy - Run Script for macOS/Linux
# This script activates the virtual environment and runs Streamlit

echo ""
echo "========================================="
echo "  AI Study Buddy - Application Launcher"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run: python3 setup.py"
    echo ""
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found."
    echo "Please configure your API key in .env file"
    echo ""
fi

# Run Streamlit
echo "Starting AI Study Buddy..."
echo ""
echo "Note: Press Ctrl+C to stop the application"
echo ""

streamlit run app.py

# Deactivate on exit
deactivate
