#!/bin/bash
# research_indexer.sh - Shell wrapper to auto-index research documents and update Wikilinks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run setup to verify/initialize venv and dependencies
source "$SCRIPT_DIR/setup_env.sh"

# Run the python script with the passed arguments
python3 "$SCRIPT_DIR/research_indexer.py" "$@"
