#!/usr/bin/env bash
# Quick start guide for Spaceship Simulator

echo "🚀 Spaceship Simulator - Quick Start"
echo "===================================="
echo ""

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please visit: https://python-poetry.org/docs/"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
poetry install --no-root

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the game, run:"
echo "  poetry run spaceship"
echo ""
echo "For more information, see README.md and DEVELOPMENT.md"
echo ""
