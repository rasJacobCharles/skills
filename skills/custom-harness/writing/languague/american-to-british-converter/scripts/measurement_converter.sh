#!/bin/bash
# measurement_converter.sh - Shell wrapper to convert US Customary measurements to Metric/UK equivalents

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run setup to verify/initialize venv
source "$SCRIPT_DIR/setup_env.sh"

# Run the python script with the passed arguments
python3 "$SCRIPT_DIR/measurement_converter.py" "$@"
