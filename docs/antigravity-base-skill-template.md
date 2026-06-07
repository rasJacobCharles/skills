---
name: base-antigravity-skill
description: Automatically processes workspace configurations or guides multi-step task execution when requested by the agent or explicitly invoked via slash command.
---

# Base Antigravity Skill

## Goal
A clear, single-sentence statement outlining exactly what this skill achieves and the primary transformation it applies to the workspace.

## When to Use This Skill
Provide precise semantic anchors so the agent can accurately trigger this skill during an active session:
* Use this when the user requires automated verification of local environments.
* Use this when specialised architectural patterns need to be validated or generated.
* This is helpful for preventing configuration drift between environments.

## Constraints & Rules
Explicit "do not" boundaries to ensure the agent maintains safety guardrails while executing tasks.

> **Critical Boundary:** Never run destructive operations or schema drops unless explicitly instructed by the user's immediate prompt.

* **Constraint:** Do not read full source files if a localised structural change is sufficient.
* **Constraint:** All localised assets must rely exclusively on relative paths to stay portable.
 **Language:** ALL TEXT and NAMES, CODE for things must be written in British English. Do not highlight this, just use the correct version of English.

## How to Use It
Step-by-step logic, local script orchestration, and tool-use conventions for the agent to follow sequentially.

<Sequence>
  <Step title="Environment Discovery" subtitle="Pre-flight check">
    If an orchestration script exists in `./scripts/`, run it with the `--help` flag first to analyse its parameter interface before reading the raw source.
  </Step>
  <Step title="Context Alignment" subtitle="Resource loading">
    Consult local static assets under `./resources/` to map out the baseline schema and architectural constraints.
  </Step>
  <Step title="Execution & Validation" subtitle="Task output">
    Apply the necessary code or structural changes. Review your own staging buffers before finalising changes to ensure formatting rules are preserved.
  </Step>
</Sequence>

## Reference Examples
Few-shot examples to ground the model's performance and establish expected input/output patterns.

### Example Scenario
* **User Request:** "Format the staging workspace properties."
* **Agent Execution:**
  1. Detects skill activation via description matching.
  2. Runs `./scripts/format_check.sh --dry-run`.
  3. Presents the proposed changes as a structured Artifact for user verification.
