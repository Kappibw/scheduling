#!/bin/bash

# Script to install research-specific requirements from the submodule
# This runs inside the container when it starts

set -e

echo "🔧 Installing research-specific requirements..."

# Check if research-code directory exists and has requirements
if [ -d "/app/research-code/requirements" ]; then
    echo "📦 Found research requirements, installing..."
    
    # Install each requirements file if it exists
    for req_file in /app/research-code/requirements/*.txt; do
        if [ -f "$req_file" ]; then
            echo "Installing from $(basename "$req_file")..."
            pip install --no-cache-dir -r "$req_file"
        fi
    done
    
    echo "✅ Research requirements installed successfully!"
else
    echo "⚠️  No research requirements found in /app/research-code/requirements/"
    echo "   Make sure your research repository has a requirements/ directory"
fi
