# sensors

Three background hooks that run automatically at session boundaries — no slash command needed. Register them in `~/.claude/settings.json` to activate for all sessions.

## `skill-usage-log`

**Trigger:** PostToolUse (whenever a skill is invoked)

Appends one tab-separated line per invocation to `~/.claude/skill-usage.log`, recording the timestamp, skill name, session ID, and any args passed. Useful for seeing which skills are popular and which are undertriggering.

## `action-review`

**Trigger:** SessionEnd, PreCompact, PostCompact

- Extracts user goals and tool-usage counts from the session transcript
- **PreCompact**: runs synchronously and outputs a summary to stdout, so key context is folded into the compaction summary and survives the context window shrink
- **SessionEnd / PostCompact**: runs in the background and saves a markdown report to `~/.claude/session-reviews/`

## `goal-eval`

**Trigger:** SessionEnd only

Runs in the background and performs three tasks:

1. **Goal evaluation** — identifies the user's primary goal and assesses whether it was accomplished (Yes / Partial / No) with supporting evidence
2. **Skill opportunity detection** — flags repeated patterns or multi-step workflows that could be encapsulated as a new reusable skill
3. **Skill gap detection** — for each existing skill that was used and fell short: if it has an `eval.md`, a `rubric.md`, and at least one fixture, it writes a new fixture that reproduces the failure scenario and appends a rubric criterion the current skill would fail

Reports are saved to `~/.claude/session-evals/`.
