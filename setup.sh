#!/bin/bash

# Automatic Setup Script for Financial Data Pipeline
# This script automates environment creation and dependency installation.

set -e

echo "=== Starting Environment Setup ==="

# 1. System Requirements Check (Ubuntu/Debian)
echo "Checking system dependencies..."

# Check for python3-venv
if ! dpkg -l | grep -q python3-venv; then
    echo "Error: python3-venv is not installed."
    echo "Please run: sudo apt update && sudo apt install python3-venv"
    exit 1
fi

# Check for sqlite3 binary (useful for debugging from terminal)
if ! command -v sqlite3 &> /dev/null; then
    echo "Warning: sqlite3 command-line tool not found."
    echo "It is recommended to install it with: sudo apt install sqlite3"
fi

# 2. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# 3. Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# 4. Upgrade pip and install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found."
    exit 1
fi

# 5. Environment configuration check
if [ ! -f ".env" ]; then
    echo "Creating .env template..."
    echo "ALPHA_VANTAGE_API_KEY=your_key_here" > .env
    echo "IMPORTANT: Update the .env file with your Alpha Vantage API key."
fi

echo "-------------------------------------------"
echo "=== Setup Completed Successfully ==="
echo "To start the application, run:"
echo "source venv/bin/activate && python main.py"
echo "-------------------------------------------"
