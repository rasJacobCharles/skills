---
fixtures: evals/fixtures/multi-agent-code-review.json
rubric: evals/rubrics/multi-agent-code-review.md
---

# Eval: Multi-Agent Code Review

This evaluation verifies the execution of the Multi-Agent Code Review skill. It loads fixtures from the central `evals/fixtures/multi-agent-code-review.json` file and evaluates agent and loop behaviors against the rubric `evals/rubrics/multi-agent-code-review.md`.

## 🧭 Calibration Guide

### C1: Agent Specialisation
- **1 (Pass):** All seven agents are instantiated and isolated. The Coordinator agent correctly directs the feedback cycles.
- **0 (Fail):** Agents are conflated, or the loop fails to terminate under constraints.

### C2: Document Isolation & Sandboxing
- **1 (Pass):** Correctly checks and verifies code against rules using sandboxed goal/fixture files on disk prior to interaction.
- **0 (Fail):** Skips local sandboxing or operates without structured documentation boundaries.

### C3: Continuous Optimisation Loop
- **1 (Pass):** Follows the loop (Code Change ➔ Eval ➔ Suggest ➔ Apply) and reports outcomes correctly with loop limits.
- **0 (Fail):** Loops indefinitely beyond 5 cycles or fails to log score histories.
