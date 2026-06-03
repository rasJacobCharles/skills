# Research AI Rubric

Score each criterion **PASS (1)** / **FAIL (0)** / **N/A**.
N/A criteria are excluded from the denominator.
Final score = sum(PASS) / sum(applicable) × 100.

---

## 1. Classification
*   **1.1 Method Classification:** Correctly classifies the user's research topic into Quantitative, Qualitative, or Mixed based on requirements.

## 2. Interactive Discovery
*   **2.1 One Question at a Time:** Asks exactly one question at a time during user interviewing.

## 3. Decision & Critique
*   **3.1 Feasibility Verdict:** Correctly recommends **Drop** for highly unfeasible ideas, or **Start** for feasible ideas.
*   **3.2 Risk & Flaw Identification:** Outlines real, concrete financial/operational risks for dropped ideas instead of confirming bias.
*   **3.3 Next Steps:** Provides actionable, specific next steps for started ideas.

## 4. Obsidian Structure
*   **4.1 Dashboard Layout:** Generates `00_Overview.md` with correct YAML frontmatter and standard wikilinks (`[[01_Research_Design]]`, etc.).
