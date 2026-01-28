#!/bin/bash

# Automatic Setup Script for Financial Data Suite
# Automates environment creation, dependency installation, and project structure.

set -e

echo "=== Starting Unified Environment Setup ==="

# 1. System Requirements Check (Ubuntu/Debian)
echo "Checking system dependencies..."

# Check for python3-venv (Required to create the virtual environment)
if ! dpkg -l | grep -q python3-venv; then
    echo "Error: python3-venv is not installed."
    echo "Please run: sudo apt update && sudo apt install python3-venv"
    exit 1
fi

# Check for sqlite3 binary (Essential for database debugging)
if ! command -v sqlite3 &> /dev/null; then
    echo "Warning: sqlite3 command-line tool not found."
    echo "It is recommended to install it with: sudo apt install sqlite3"
fi

# 2. Project Structure Integrity
echo "Ensuring project structure..."
mkdir -p data
touch src/__init__.py
touch tests/__init__.py

# 3. Virtual Environment Management
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# 4. Dependency Installation
echo "Activating virtual environment and installing packages..."
source venv/bin/activate
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found. Cannot install dependencies."
    exit 1
fi

# 5. Environment Configuration
if [ ! -f ".env" ]; then
    echo "Creating .env template..."
    echo "ALPHA_VANTAGE_API_KEY=your_key_here" > .env
    echo "IMPORTANT: Add your Alpha Vantage API key to the .env file."
fi

echo "-------------------------------------------"
echo "=== Setup Completed Successfully ==="
echo "To start, run: source venv/bin/activate"
echo "Then execute: python main.py"
echo "-------------------------------------------"
