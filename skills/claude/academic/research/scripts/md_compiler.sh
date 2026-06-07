#!/bin/bash
# md_compiler.sh - Shell wrapper to compile individual chapter markdown files into a single master report

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run setup to verify/initialize venv and dependencies
source "$SCRIPT_DIR/setup_env.sh"

# Run the python script with the passed arguments
python3 "$SCRIPT_DIR/md_compiler.py" "$@"
