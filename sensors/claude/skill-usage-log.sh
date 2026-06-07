#!/usr/bin/env bash
# Sensor: skill-usage-log
# Triggered on: PostToolUse (matcher: Skill)
#
# Appends one line per skill invocation to ~/.claude/skill-usage.log so you can
# see which skills are popular and which are undertriggering.
#
# Log format (tab-separated):
#   2026-06-05T10:30:00Z  standup  session=abc12345  args=(none)

set -euo pipefail

command -v jq >/dev/null 2>&1 || exit 0

INPUT=$(cat)

SKILL_NAME=$(echo "$INPUT" | jq -r '.tool_input.skill // "unknown"' 2>/dev/null || echo "unknown")
ARGS=$(echo "$INPUT"       | jq -r '.tool_input.args  // "(none)"'  2>/dev/null || echo "(none)")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id        // "unknown"' 2>/dev/null || echo "unknown")

BASE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.claude}"
LOG_FILE="$BASE_DIR/skill-usage.log"
mkdir -p "$(dirname "$LOG_FILE")"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

printf '%s\t%s\tsession=%s\targs=%s\n' \
  "$TIMESTAMP" "$SKILL_NAME" "${SESSION_ID:0:8}" "$ARGS" \
  >> "$LOG_FILE"

exit 0
