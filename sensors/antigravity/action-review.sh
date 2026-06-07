#!/usr/bin/env bash
# Sensor: action-review (Antigravity version)
# Triggered on: Stop
#
# Reviews all actions taken in the session.
# Saves markdown to $BASE_DIR/session-reviews/

set -euo pipefail

# Guard deps
command -v jq  >/dev/null 2>&1 || { echo "action-review: jq not found" >&2; exit 0; }
command -v agy >/dev/null 2>&1 || { echo "action-review: agy not found" >&2; exit 0; }

INPUT=$(cat)
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcriptPath // empty' 2>/dev/null || true)
SESSION_ID=$(echo "$INPUT"      | jq -r '.conversationId // "unknown"' 2>/dev/null || echo "unknown")
EVENT=$(echo "$INPUT"           | jq -r '.event          // "Stop"' 2>/dev/null || echo "Stop")

[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# --- Extract transcript info ---
# Antigravity transcript.jsonl format:
# User goals: first 6 non-meta user messages (type == "USER_INPUT")
USER_GOALS=$(jq -r '
  select(.type == "USER_INPUT") |
  .content | gsub("\\n"; " ") | .[0:250]
' "$TRANSCRIPT_PATH" 2>/dev/null \
  | grep -v '^[[:space:]]*$' \
  | head -6 \
  || echo "(unable to extract)")

# Tool usage: count by tool name from PLANNER_RESPONSE tool_calls array
TOOL_COUNTS=$(jq -r '
  select(.type == "PLANNER_RESPONSE") |
  if .tool_calls then .tool_calls[].name else empty end
' "$TRANSCRIPT_PATH" 2>/dev/null \
  | sort | uniq -c | sort -rn \
  | head -15 \
  | sed 's/^ *//' \
  || echo "(unable to extract)")

# --- Build prompt ---
PROMPT_FILE=$(mktemp /tmp/action-review-XXXXXX.txt)

{
  printf 'You are reviewing a Google Antigravity session transcript.\n\n'
  printf 'Event: %s\n' "$EVENT"
  printf 'Session ID: %s\n\n' "$SESSION_ID"
  printf 'User goals/requests (from first 6 user messages):\n'
  printf '%s\n\n' "$USER_GOALS"
  printf 'Tool usage (name × count):\n'
  printf '%s\n\n' "$TOOL_COUNTS"
  printf 'Write a structured markdown action summary. Be specific and factual. Under 300 words.\n\n'
  printf '# Action Review — %s\n\n' "$EVENT"
  printf '## Goals Identified\n'
  printf 'What was the user trying to accomplish?\n\n'
  printf '## Actions Taken\n'
  printf 'Group by category — File Changes | Commands Executed | Reads / Research | External Tools\n\n'
  printf '## Outcomes\n'
  printf 'What was produced, fixed, found, or deployed?\n\n'
  printf '## Incomplete or Unresolved\n'
  printf 'Anything not finished, or open questions remaining?\n'
} > "$PROMPT_FILE"

PROMPT=$(cat "$PROMPT_FILE")
rm -f "$PROMPT_FILE"

# --- Run analysis ---
BASE_DIR="${ANTIGRAVITY_PLUGIN_DATA:-$HOME/.gemini/antigravity}"
REVIEW_DIR="$BASE_DIR/session-reviews"
mkdir -p "$REVIEW_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REVIEW_FILE="$REVIEW_DIR/${TIMESTAMP}-${SESSION_ID:0:8}-${EVENT}.md"

run_agy() {
  agy -p "$PROMPT" --cwd "$(pwd)" 2>/dev/null
}

# Run in background
(run_agy > "$REVIEW_FILE" || true) &

exit 0
