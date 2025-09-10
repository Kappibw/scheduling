#!/bin/bash

# Script to add a research repository as a git submodule
# Usage: ./scripts/add-research-repo.sh <repository-url>

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <repository-url>"
    echo ""
    echo "Example:"
    echo "  $0 https://github.com/yourusername/robot-scheduling-research.git"
    echo "  $0 git@github.com:yourusername/robot-scheduling-research.git"
    exit 1
fi

REPO_URL=$1

echo "🔗 Adding research repository as submodule..."
echo "Repository: $REPO_URL"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: This script must be run from the root of a git repository"
    exit 1
fi

# Check if research-code directory already exists
if [ -d "research-code" ]; then
    echo "❌ Error: research-code directory already exists"
    echo "If you want to replace it, please remove it first:"
    echo "  rm -rf research-code"
    echo "  git rm research-code"
    exit 1
fi

# Add the submodule
echo "Adding submodule..."
git submodule add "$REPO_URL" research-code

echo ""
echo "✅ Research repository added as submodule!"
echo ""
echo "Next steps:"
echo "  1. Run './scripts/setup.sh' to initialize the environment"
echo "  2. Or run 'make setup' to initialize everything"
echo ""
echo "To update the research code later:"
echo "  git submodule update --remote research-code"
