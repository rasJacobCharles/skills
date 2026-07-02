# Vault Ingester Rubric

Score each criterion **PASS (1)** / **FAIL (0)** / **N/A**.
N/A criteria are excluded from the denominator.
Final score = sum(PASS) / sum(applicable) × 100.

---

## 1. Document Structure & Frontmatter
*   **1.1 Frontmatter Metadata:** Includes valid YAML frontmatter with tags, research_type, sources, and parent link.
*   **1.2 Bolded System Overview:** Starts with a 1-2 paragraph overview fully bolded.
*   **1.3 Five-Section Structure:** Section headers are numbered 1 through 5 matching the required template.

## 2. Content & Completeness
*   **2.1 Comparison Table:** Section 4 contains a markdown table comparing metrics, baselines, or features.
*   **2.2 Setup Commands:** Section 5 includes actionable conda/pip setup commands.

## 3. Linkage & Hierarchy
*   **3.1 Parent Page Link:** The parent page is updated to include the link back to the new file, and the frontmatter parent points to the parent page.
*   **3.2 Interactive Parent Prompt:** If the parent page is not specified, the agent asks the user to clarify/confirm the parent.

## 4. Spelling & Style
*   **4.1 British English spelling:** All generated content adheres strictly to British English spelling (e.g. *behaviour*, *optimise*, *prioritise*, *initialise*, *capitalised*, *synthesise*, *analyse*).
