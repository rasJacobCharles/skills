#!/usr/bin/env bash
# Sensor: goal-eval (Antigravity version)
# Triggered on: Stop
#
# Three-part analysis:
#   1. Goal evaluation  — did the session accomplish what the user asked?
#   2. Skill opportunities — patterns worth encapsulating as reusable skills
#   3. Existing skill gaps — if a skill was used and fell short, AND it has an
#      eval + rubric, adds a new fixture that exposes the gap and a rubric entry
#      that the current skill would fail.
#
# Saves a markdown report to $BASE_DIR/session-evals/
# Runs in the background so it does not block the session from ending.

set -euo pipefail

command -v jq  >/dev/null 2>&1 || { echo "goal-eval: jq not found" >&2; exit 0; }
command -v agy >/dev/null 2>&1 || { echo "goal-eval: agy not found" >&2; exit 0; }

INPUT=$(cat)
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcriptPath // empty' 2>/dev/null || true)
SESSION_ID=$(echo "$INPUT"      | jq -r '.conversationId // "unknown"' 2>/dev/null || echo "unknown")

[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$PLUGIN_DIR/skills"
EVALS_DIR="$PLUGIN_DIR/evals"

BASE_DIR="${ANTIGRAVITY_PLUGIN_DATA:-$HOME/.gemini/antigravity}"
EVAL_REPORT_DIR="$BASE_DIR/session-evals"
mkdir -p "$EVAL_REPORT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT_FILE="$EVAL_REPORT_DIR/${TIMESTAMP}-${SESSION_ID:0:8}.md"

# Gather previous session evaluations (last 3 reports for history/memory)
PREVIOUS_EVALS=""
if [[ -d "$EVAL_REPORT_DIR" ]]; then
  PREVIOUS_FILES=$(find "$EVAL_REPORT_DIR" -name "*.md" -type f | sort -r | head -3 2>/dev/null || true)
  if [[ -n "$PREVIOUS_FILES" ]]; then
    for f in $PREVIOUS_FILES; do
      PREVIOUS_EVALS+="### $(basename "$f")"$'\n'
      PREVIOUS_EVALS+="$(head -n 15 "$f")"$'\n\n'
    done
  fi
fi
if [[ -z "$PREVIOUS_EVALS" ]]; then
  PREVIOUS_EVALS="(no previous session evaluations found)"
fi

# --- Extract transcript info ---
# Antigravity transcript.jsonl format:
# User messages (type == "USER_INPUT")
USER_MSGS=$(jq -r '
  select(.type == "USER_INPUT") |
  .content | gsub("\\n"; " ") | .[0:300]
' "$TRANSCRIPT_PATH" 2>/dev/null \
  | grep -v '^[[:space:]]*$' \
  | head -8 \
  || echo "(unable to extract)")

# Last 6 model messages (source == "MODEL" or type == "PLANNER_RESPONSE")
ASSISTANT_MSGS=$(jq -r '
  select(.source == "MODEL" or .type == "PLANNER_RESPONSE") |
  (.content // .thinking // empty) | gsub("\\n"; " ") | .[0:300]
' "$TRANSCRIPT_PATH" 2>/dev/null \
  | grep -v '^[[:space:]]*$' \
  | tail -6 \
  || echo "(unable to extract)")

# Tool usage: count by tool name from PLANNER_RESPONSE tool_calls array
TOOL_COUNTS=$(jq -r '
  select(.type == "PLANNER_RESPONSE") |
  if .tool_calls then .tool_calls[].name else empty end
' "$TRANSCRIPT_PATH" 2>/dev/null \
  | sort | uniq -c | sort -rn | head -20 \
  | sed 's/^ *//' \
  || echo "(none)")

# Gather available skills and their eval status
SKILLS_INFO=""
if [[ -d "$SKILLS_DIR" ]]; then
  for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    has_eval="no"
    has_fixtures="no"
    [[ -f "$skill_dir/eval.md" ]] && has_eval="yes"
    [[ -d "$EVALS_DIR/$skill_name/fixtures" ]] && ls "$EVALS_DIR/$skill_name/fixtures/"* >/dev/null 2>&1 && has_fixtures="yes"
    SKILLS_INFO+="  - $skill_name (eval: $has_eval, fixtures: $has_fixtures)"$'\n'
  done
fi

# --- Build prompt ---
PROMPT_FILE=$(mktemp /tmp/goal-eval-XXXXXX.txt)

{
  printf 'You are a session quality evaluator for Google Antigravity. Analyse this session and complete three tasks.\n\n'

  printf '## Session context\n'
  printf 'Session ID: %s\n' "$SESSION_ID"
  printf 'Plugin directory: %s\n' "$PLUGIN_DIR"
  printf 'Skills directory: %s\n' "$SKILLS_DIR"
  printf 'Evals directory:  %s\n\n' "$EVALS_DIR"

  printf '## Previous Session Evaluations (History/Memory)\n'
  printf '%s\n\n' "$PREVIOUS_EVALS"

  printf '## Available skills\n'
  printf '%s\n' "$SKILLS_INFO"
  printf 'To avoid overloading the context window, do not pre-load the files of all skills. Explore the skills directory (`skills/<skill-name>`) using the Read tool only when a skill is relevant to a detected gap.\n\n'

  printf '## User messages (first 8, up to 300 chars each)\n'
  printf '%s\n\n' "$USER_MSGS"

  printf '## Final assistant messages (last 6, up to 300 chars each)\n'
  printf '%s\n\n' "$ASSISTANT_MSGS"

  printf '## Tool usage (name × count)\n'
  printf '%s\n\n' "$TOOL_COUNTS"

  cat << 'STATIC'
---

## Task 1 — Goal Evaluation
Identify the user's primary goal from the first user message(s).
Assess: Was the goal accomplished? (Yes / Partial / No)
Provide specific evidence. Note any gaps or issues that remain.

## Task 2 — Skill Opportunity Analysis
Identify any repeated patterns, multi-step workflows, or complex interactions that
could be encapsulated as a reusable skill. Classify each candidate into one of these 9 categories:
1. Library and API reference (Gotchas, CLI wrappers, SDK instructions)
2. Product verification (Playwright/headless UI drivers, tmux TTY assertions)
3. Data fetching and analysis (Monitoring, datasource queries, Datadog/Grafana)
4. Business process and team automation (Standups, tickets, Slack integrations)
5. Code scaffolding and templates (Migration files, boilerplate templates)
6. Code quality and review (Adversarial review hooks, code style, testing guidelines)
7. CI/CD and deployment (Smoke tests, rollout babysitting, cherry-picks)
8. Runbooks (Symptom-to-tool investigations, log correlators)
9. Infrastructure operations (Resource cleanups, dependency approvals)

For each candidate:
- Suggested skill name and one-line description
- Category (from the list above)
- Specific pattern observed
- Opportunity rating: High / Medium / Low

## Task 3 — Existing Skill Gap Detection
For each available skill, assess whether it was used (directly invoked or its
workflow followed manually). For each skill that was used and showed a gap, bug,
or missing behaviour:
STATIC

  printf '\n1. Read the skill file: %s/<skill-name>/SKILL.md\n' "$SKILLS_DIR"
  printf '2. Check for eval:     %s/<skill-name>/eval.md\n' "$SKILLS_DIR"
  printf '3. Check for rubric:   %s/<skill-name>/rubric.md\n' "$EVALS_DIR"
  printf '4. List existing fixtures in: %s/<skill-name>/fixtures/\n' "$EVALS_DIR"

  printf '\nIf the skill has both an eval AND a rubric AND existing fixtures:\n'
  printf 'a) Create a new fixture at %s/<skill-name>/fixtures/gap-<short-slug>.<ext>\n' "$EVALS_DIR"
  printf '   where <ext> matches the extension of existing fixtures in that directory\n'
  printf '   (e.g. .php for create-tests fixtures, .md for most others).\n'
  printf '   Match the format and level of detail of the existing fixtures exactly.\n'
  printf 'b) Append a new rubric criterion to %s/<skill-name>/rubric.md that\n' "$EVALS_DIR"
  printf '   captures what the skill should have done but did not. The criterion must be\n'
  printf '   written so the current skill behaviour would FAIL it. Use the same table and\n'
  printf '   numbering style as the existing rubric entries.\n'

  printf '\n## Output format\n'
  printf 'Output your full markdown report as plain text (do not use the Write tool for the report itself).\n'
  printf 'Use the Write tool only for gap fixture and rubric files.\n\n'

  cat << 'STATIC'
Structure:
# Session Goal Evaluation
## Goal: <one line>
## Outcome: Yes / Partial / No
## Evidence
## Remaining gaps

# Skill Opportunity Candidates
(table: Skill Name | Category | Pattern | Rating)

# Existing Skill Gaps
(for each gap: skill name, what went wrong, action taken)

# Files Created or Modified
(list any fixture or rubric files written)
STATIC
} > "$PROMPT_FILE"

PROMPT=$(cat "$PROMPT_FILE")
rm -f "$PROMPT_FILE"

# --- Run in background so Stop event is not delayed ---
(
  agy -p "$PROMPT" --cwd "$(pwd)" 2>/dev/null > "$REPORT_FILE" || true
) &

exit 0
