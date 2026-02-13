#!/bin/bash
# Setup script for Emotion MCP Server

echo "Setting up Emotion MCP Server..."

# Check Python version
python --version

# Create virtual environment
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install mcp datasets pydantic

# Run tests
python test_tools.py

