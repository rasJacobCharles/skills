---
skill: skills/custom-harness/automation/message-bus/SKILL.md
fixtures: evals/fixtures/message-bus.json
rubric: evals/rubrics/message-bus.md
---

# Eval: Asynchronous AI Message Bus

This evaluation verifies the agent's compliance with the Asynchronous AI Message Bus pattern, specifically measuring non-blocking task ingestion, deterministic sorting based on task timestamps, strict de-queuing policy upon execution start, and event broadcasting to multiple active subscribers.

It loads test fixtures from the central `evals/fixtures/message-bus.json` file and scores against the rubric `evals/rubrics/message-bus.md`.

## 🧭 Calibration Guide

### C1: Task Ingestion
- **1 (Pass):** Ingests tasks into a holding queue without locking or blocking the main execution thread, and explains the non-blocking design.
- **0 (Fail):** Commences processing synchronously, locking the main execution path, or fails to define a holding queue.

### C2: Ordering & Identity Mechanics
- **1 (Pass):** Injects a distinct `timestamp` structural attribute into the payload identification schema of every task, and sorts the queue deterministically by timestamp.
- **0 (Fail):** Fails to inject timestamps, or processes tasks out of order without deterministic sorting.

### C3: Lifecycle Management (Strict De-queuing)
- **1 (Pass):** Removes the active task from the polling queue immediately when execution starts to prevent concurrent double-execution.
- **0 (Fail):** Retains tasks in the active queue during execution, risking double-execution by other worker threads.

### C4: Subscription & Broadcast Model
- **1 (Pass):** Registers and broadcasts task completion events to multiple registered subscriber functions in a 1-to-many topology.
- **0 (Fail):** Restricts execution to a single point-to-point worker delivery, or fails to broadcast completion events.
