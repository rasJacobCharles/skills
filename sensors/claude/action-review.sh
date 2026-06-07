#!/usr/bin/env bash
# Sensor: action-review
# Triggered on: SessionEnd, PreCompact, PostCompact
#
# Reviews all actions taken in the session.
# - PreCompact: runs synchronously, outputs to stdout so key context survives compaction.
# - SessionEnd / PostCompact: runs in background, saves markdown to ~/.claude/session-reviews/

set -euo pipefail

# Guard deps
command -v jq    >/dev/null 2>&1 || { echo "action-review: jq not found" >&2; exit 0; }
command -v claude >/dev/null 2>&1 || { echo "action-review: claude not found" >&2; exit 0; }

INPUT=$(cat)
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || true)
SESSION_ID=$(echo "$INPUT"     | jq -r '.session_id     // "unknown"' 2>/dev/null || echo "unknown")
EVENT=$(echo "$INPUT"          | jq -r '.hook_event_name // "SessionEnd"' 2>/dev/null || echo "SessionEnd")

[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# --- Extract transcript info ---
# Claude Code JSONL format: each line has top-level "type" ("user"/"assistant"),
# with content at .message.content (string or array of blocks).
# Tool uses live inside assistant message content blocks.

# User goals: first 6 non-meta user messages, collapsed to one line each.
USER_GOALS=$(jq -r '
  select(.type == "user" and ((.isMeta // false) | not)) |
  if (.message.content | type) == "array" then
    .message.content[] | select(.type == "text") | .text | gsub("\\n"; " ") | .[0:250]
  elif (.message.content | type) == "string" then
    .message.content | gsub("\\n"; " ") | .[0:250]
  else empty end
' "$TRANSCRIPT_PATH" 2>/dev/null \
  | grep -v '^[[:space:]]*$' \
  | head -6 \
  || echo "(unable to extract)")

# Tool usage: count by tool name from assistant message content blocks.
# Tool uses only appear in array content; string content has none — yield empty.
TOOL_COUNTS=$(jq -r '
  select(.type == "assistant") |
  if (.message.content | type) == "array" then
    .message.content[] | select(.type == "tool_use") | .name
  else empty end
' "$TRANSCRIPT_PATH" 2>/dev/null \
  | sort | uniq -c | sort -rn \
  | head -15 \
  | sed 's/^ *//' \
  || echo "(unable to extract)")

# --- Build prompt (safe: dynamic content written via printf %s, never heredoc-expanded) ---

# Build prompt into a temp file, then immediately capture into a variable and
# delete the file. This avoids a race where the EXIT trap removes the file
# before a background subshell can read it.
PROMPT_FILE=$(mktemp /tmp/action-review-XXXXXX.txt)

{
  printf 'You are reviewing a Claude Code session transcript.\n\n'
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

BASE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.claude}"
REVIEW_DIR="$BASE_DIR/session-reviews"
mkdir -p "$REVIEW_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REVIEW_FILE="$REVIEW_DIR/${TIMESTAMP}-${SESSION_ID:0:8}-${EVENT}.md"

run_claude() {
  claude -p "$PROMPT" \
    --output-format text \
    --bare \
    --no-session-persistence \
    --max-budget-usd 0.05 \
    2>/dev/null
}

if [[ "$EVENT" == "PreCompact" ]]; then
  # Synchronous: stdout is captured into the compaction context summary
  run_claude || true
else
  # Background: save to file
  (run_claude > "$REVIEW_FILE" || true) &
fi

exit 0
