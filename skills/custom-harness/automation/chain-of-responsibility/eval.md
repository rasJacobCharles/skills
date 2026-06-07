---
fixtures: evals/fixtures/chain-of-responsibility.json
rubric: evals/rubrics/chain-of-responsibility.md
---

# Eval: Chain of Responsibility (CoR) Workflow

This evaluation verifies the agent's compliance with the Chain of Responsibility (CoR) workflow pattern, specifically measuring context initialization, traversal tracking, loop prevention, and filesystem-based memory updates.

It loads test fixtures from the central `evals/fixtures/chain-of-responsibility.json` file and scores against the rubric `evals/rubrics/chain-of-responsibility.md`.

## 🧭 Calibration Guide

### C1: State & Telemetry Inception
- **1 (Pass):** Correctly parses input request parameters, initializes execution telemetry counters, and instantiates the `SharedContext` structure before running check tasks.
- **0 (Fail):** Commences processing without initializing memory state or tracking run counts.

### C2: Linear Traversal & Chain Forwarding
- **1 (Pass):** Follows the `next_handler` property of each handler sequentially, logging execution details for each step in the history log array.
- **0 (Fail):** Skips handlers in the chain or runs them out of order.

### C3: Short-Circuiting & Loop Prevention
- **1 (Pass):** Halts pipeline processing immediately if a validation error occurs or if a recursive loop (execution count of a handler reaches 3) is detected.
- **0 (Fail):** Fails to check run counts or permits execution to continue despite errors or loop cycles.

### C4: Progressive Disclosure & Filesystem Model
- **1 (Pass):** Uses progressive disclosure by accessing specific handler instructions via linked files on-demand, and reads/writes the context file (`context.json`) on disk.
- **0 (Fail):** Expects all instructions to be loaded in context at once, or fails to store state changes in the persistent context file.
