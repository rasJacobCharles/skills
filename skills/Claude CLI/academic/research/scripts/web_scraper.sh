#!/bin/bash
# web_scraper.sh - Shell wrapper to download and extract clean content from web pages

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run setup to verify/initialize venv and dependencies
source "$SCRIPT_DIR/setup_env.sh"

# Run the python script with the passed arguments
python3 "$SCRIPT_DIR/web_scraper.py" "$@"
