---
fixtures: evals/fixtures/technical-archaeology.json
rubric: evals/rubrics/technical-archaeology.md
---

# Eval: Technical Archaeology

This eval verifies the behavior of the Technical Archaeology skill. It loads fixtures from the central `evals/fixtures/technical-archaeology.json` file and scores against `evals/rubrics/technical-archaeology.md`.

## 🧭 Calibration Guide

### C1: Discovery & Gap Detection
- **1 (Pass):** Correctly lists specific, logical architectural gaps based on the codebase scan.
- **0 (Fail):** Fails to identify any gaps or immediately outputs the TDD without scanning first.

### C2: Interactive Discovery
- **1 (Pass):** Asks exactly one question at a time.
- **0 (Fail):** Asks multiple questions at once or dumps a full questionnaire.

### C3: Template Compliance
- **1 (Pass):** The final TDD contains all 6 required sections in order, including a valid Mermaid diagram.
- **0 (Fail):** Misses major sections or lacks a valid Mermaid diagram.
