---
skill: skills/claude/academic/vault-ingester/SKILL.md
fixtures: evals/fixtures/vault-ingester.json
rubric: evals/rubrics/vault-ingester.md
---

# Eval: Vault Ingester

This eval verifies the behavior of the Vault Ingester skill. It loads fixtures from the central `evals/fixtures/vault-ingester.json` file and scores against `evals/rubrics/vault-ingester.md`.

## 🧭 Calibration Guide

### C1: Document Structure
- **1 (Pass):** Correctly numbers sections 1 through 5, starts with a fully bolded System Overview section, and contains correct frontmatter tags, research_type, sources, and parent.
- **0 (Fail):** Omit frontmatter, does not bold System Overview, or deviates from the 5-section structure.

### C2: Comparison Table
- **1 (Pass):** Generates a markdown table in Section 4 comparing metrics, baselines, or features.
- **0 (Fail):** Omit the table.

### C3: Actionable Setup
- **1 (Pass):** Includes conda/pip setup commands in Section 5.
- **0 (Fail):** Omit or provides incomplete commands.

### C4: Parent Page Linkage
- **1 (Pass):** Updates the parent page to include a link to the new file, and sets the correct parent wikilink in frontmatter.
- **0 (Fail):** Omit parent update.

### C5: British English Adherence
- **1 (Pass):** Uses British English spelling consistently throughout the note (e.g. *behaviour*, *optimise*, *prioritise*, *initialise*, *capitalised*, *synthesise*, *analyse*).
- **0 (Fail):** Uses US English spelling anywhere in the output.
