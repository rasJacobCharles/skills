#!/bin/bash
# setup_env.sh - Setup python virtual environment and install dependencies locally

# Resolve the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install Python 3 and try again." >&2
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment." >&2
        exit 1
    fi
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Check if packages are installed (using requirements.txt hashes/list or just install them)
# We check if a marker file exists to avoid running pip install every time
MARKER_FILE="$VENV_DIR/.dependencies_installed"
if [ ! -f "$MARKER_FILE" ]; then
    echo "Installing required Python packages..."
    python3 -m pip install --upgrade pip
    python3 -m pip install youtube-transcript-api pypdf python-docx beautifulsoup4
    
    if [ $? -eq 0 ]; then
        touch "$MARKER_FILE"
        echo "Dependencies installed successfully."
    else
        echo "Warning: Some dependencies failed to install. Tools might have limited functionality." >&2
    fi
fi
