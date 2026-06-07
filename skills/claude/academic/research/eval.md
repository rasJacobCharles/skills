---
fixtures: evals/fixtures/research.json
rubric: evals/rubrics/research.md
---

# Eval: Research AI

This eval verifies the behavior of the Research AI skill. It loads fixtures from the central `evals/fixtures/research.json` file and scores against `evals/rubrics/research.md`.

## 🧭 Calibration Guide

### C1: Classification
- **1 (Pass):** Correctly classifies the methodology as Quantitative, Qualitative, or Mixed and provides a sound explanation.
- **0 (Fail):** Incorrect classification.

### C2: Interactive Discovery
- **1 (Pass):** Asks exactly one question at a time.
- **0 (Fail):** Asks multiple questions at once.

### C3: Decision & Critique
- **1 (Pass):** Correctly recommends Drop for unfeasible ideas (detailing risks) and Start for feasible ideas (with actionable next steps).
- **0 (Fail):** Incorrect recommendation or fails to provide solid risk/action details.

### C4: Obsidian Structure
- **1 (Pass):** Generates `00_Overview.md` with correct YAML frontmatter and standard wikilinks.
- **0 (Fail):** Omit frontmatter or wikilinks.
