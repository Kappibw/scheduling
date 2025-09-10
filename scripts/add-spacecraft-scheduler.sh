#!/bin/bash

# Script to add the spacecraft scheduler repository as a git submodule
# Usage: ./scripts/add-spacecraft-scheduler.sh <repository-url>

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <repository-url>"
    echo ""
    echo "Example:"
    echo "  $0 https://github.com/yourusername/spacecraft_scheduler.git"
    echo "  $0 git@github.com:yourusername/spacecraft_scheduler.git"
    exit 1
fi

REPO_URL=$1

echo "🚀 Adding spacecraft scheduler repository as submodule..."
echo "Repository: $REPO_URL"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: This script must be run from the root of a git repository"
    exit 1
fi

# Check if spacecraft_scheduler directory already exists
if [ -d "spacecraft_scheduler" ]; then
    echo "❌ Error: spacecraft_scheduler directory already exists"
    echo "If you want to replace it, please remove it first:"
    echo "  rm -rf spacecraft_scheduler"
    echo "  git rm spacecraft_scheduler"
    exit 1
fi

# Add the submodule
echo "Adding submodule..."
git submodule add "$REPO_URL" spacecraft_scheduler

echo ""
echo "✅ Spacecraft scheduler repository added as submodule!"
echo ""
echo "Next steps:"
echo "  1. Run 'make build' to build the container with dependencies"
echo "  2. Run 'make up' to start the development environment"
echo ""
echo "To update the spacecraft scheduler code later:"
echo "  git submodule update --remote spacecraft_scheduler"
