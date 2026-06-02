#!/bin/bash
# tdd-dig.sh - Shell wrapper to scan a directory and interactively quiz the user to build a TDD.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run setup to verify/initialize venv
source "$SCRIPT_DIR/setup_env.sh"

# Run the python script with the passed arguments
python3 "$SCRIPT_DIR/tdd_dig.py" "$@"
