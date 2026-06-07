# Pipeline Integration Examples

These examples illustrate how the Chain of Responsibility (CoR) pattern is structured and sequenced using configuration profiles and the Shared Context filesystem model:

---

## 🧼 Example 1: Text Cleaning Pipeline
This pipeline runs two successive operations on raw user-submitted text: stripping outer whitespace and replacing forbidden profanity.
*   **Pipeline Setup**: **[pipeline.yaml](clean_text_pipeline/pipeline.yaml)**
*   **State History File**: **[context.json](clean_text_pipeline/context.json)**

---

## 🔍 Example 2: Code Review Pipeline
This pipeline runs syntax check, static analysis, and mock checking.
*   **Pipeline Setup**: **[pipeline.yaml](code_review_pipeline/pipeline.yaml)**
*   **State History File**: **[context.json](code_review_pipeline/context.json)**
