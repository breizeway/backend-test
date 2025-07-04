#!/bin/bash

# Backend Test Setup Script
echo "Setting up Backend Test development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp env.example .env
    echo "Please update .env file with your configuration values."
fi

# Initialize database
echo "Initializing database..."
export FLASK_APP=app.py
flask db init || true
flask db migrate -m "Initial migration" || true
flask db upgrade || true

echo "Setup completed successfully!"
echo ""
echo "To run the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the application: python app.py"
echo "3. Visit http://localhost:5000/graphql for GraphQL explorer"
echo "4. Visit http://localhost:5000/health for health check"
echo ""
echo "For Docker development:"
echo "1. Run: docker-compose up"
echo "2. Visit http://localhost:5000/graphql"
echo "3. Visit http://localhost:8080 for Adminer (DB admin)" 