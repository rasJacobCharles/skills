---
fixtures: evals/fixtures/american-to-british-converter.json
rubric: evals/rubrics/american-to-british-converter.md
---

# Eval: American to British English Converter

This eval verifies the behavior of the American to British English Converter skill. It loads fixtures from the central `evals/fixtures/american-to-british-converter.json` file and scores against `evals/rubrics/american-to-british-converter.md`.

## 🧭 Calibration Guide

### C1: Spelling & Vocabulary
- **1 (Pass):** Correctly converts spelling patterns (e.g. `-ize` -> `-ise`, double L in traveler, `color` -> `colour`) and vocabulary words (e.g. `elevator` -> `lift`).
- **0 (Fail):** Leaves US spellings or terms unmodified.

### C2: Case & Exception Handling
- **1 (Pass):** Preserves word casing pattern exactly and leaves exception words (`size`, `seize`) completely untouched.
- **0 (Fail):** Fails case preservation or alters exception words.

### C3: Measurements
- **1 (Pass):** Correctly converts customary units to metric equivalents with accurate calculations.
- **0 (Fail):** Misses unit conversions or has major math errors.
