#!/bin/bash
# video_transcriber.sh - Shell wrapper for transcribing video files or YouTube links

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run setup to verify/initialize venv and dependencies
source "$SCRIPT_DIR/setup_env.sh"

# Run the python script with the passed arguments
python3 "$SCRIPT_DIR/video_transcriber.py" "$@"
