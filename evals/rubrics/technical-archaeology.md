# Technical Archaeology Rubric

Score each criterion **PASS (1)** / **FAIL (0)** / **N/A**.
N/A criteria are excluded from the denominator.
Final score = sum(PASS) / sum(applicable) × 100.

---

## 1. Discovery & Gap Detection
*   **1.1 Identification of Gaps:** The skill correctly identifies missing components, system boundaries, and design details from a codebase scan result.
*   **1.2 Initial Action:** Proposes scanning phase or processes scanned metadata before prompting for design outputs.

## 2. Interactive Discovery
*   **2.1 One Question at a Time:** The skill asks exactly one question at a time during the discovery dialogue.
*   **2.2 Probing Reasoning:** The skill asks follow-up or clarifying questions about trade-offs or stacks rather than accepting simple definitions.

## 3. Template Compliance
*   **3.1 Layout Structure:** The final compiled TDD contains all 6 required template sections in order (Metadata, 1. Introduction, 2. System Architecture, 3. Data & Storage, 4. Component Design, 5. Trade-Offs, 6. Risks & Roadmap).
*   **3.2 Diagram Verification:** The TDD includes a valid, syntactically correct Mermaid diagram representing the high-level architecture.
