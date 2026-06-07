# Antigravity Sensors

Background hooks for Google Antigravity that run automatically at session boundaries.

## Hook Events and Registration

Antigravity executes these scripts via triggers defined in a `hooks.json` configuration file. You can register them globally by saving this configuration to `~/.gemini/config/hooks.json` or locally for a workspace under `.agents/hooks.json`.

See [hooks.json](hooks.json) for the standard registration.

## `skill-usage-log`

**Trigger:** `PostToolUse` (matching `"Skill"` tool or similar)

Logs skill usage details (timestamp, skill name, session ID, and args) to `$ANTIGRAVITY_PLUGIN_DATA/skill-usage.log` (defaulting to `~/.gemini/antigravity/skill-usage.log`).

## `action-review`

**Trigger:** `Stop`

Reviews the entire session's tool invocations and user goals to output a comprehensive markdown review to `$ANTIGRAVITY_PLUGIN_DATA/session-reviews/`.

## `goal-eval`

**Trigger:** `Stop`

Evaluates user goal accomplishment, identifies new skill candidate opportunities, and writes automated gap fixtures and rubric updates to the skills repo when existing skills fall short. Saves reports to `$ANTIGRAVITY_PLUGIN_DATA/session-evals/`.
