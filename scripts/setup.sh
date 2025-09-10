#!/bin/bash

# Robot Scheduling Research Environment Setup Script
# This script initializes the research environment with git submodules

set -e

echo "🚀 Setting up Robot Scheduling Research Environment"
echo "=================================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: This script must be run from the root of a git repository"
    exit 1
fi

# Check if research-code submodule exists
if [ ! -d "research-code" ]; then
    echo "📋 Research code submodule not found."
    echo "Please add your research repository as a submodule:"
    echo ""
    echo "  git submodule add <your-research-repo-url> research-code"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "✅ Research code submodule found"

# Initialize and update submodules
echo "🔄 Initializing and updating submodules..."
git submodule update --init --recursive

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p results test_cases logs

# Build Docker images
echo "🐳 Building Docker images..."
docker-compose -f docker-compose.yml build

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Run 'make up' to start the research environment"
echo "  2. Access Jupyter Lab at http://localhost:8888"
echo "  3. Or use Cursor with 'Remote-Containers: Reopen in Container'"
echo ""
echo "Available commands:"
echo "  make help     - Show all available commands"
echo "  make up       - Start research environment"
echo "  make research - Run algorithm research"
echo "  make jupyter  - Show Jupyter Lab info"
