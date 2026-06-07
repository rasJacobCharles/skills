# Framework for Skill Evaluations

## 1. Core Principles

*   **Objective Over Subjective**: Write assertion criteria that can be definitively checked by an LLM evaluator or a script. Avoid vague quality judgements.
*   **Evidence-Based**: Every grading result must cite direct, quoted, or observable evidence from the generated output.
*   **Rubric-Driven & Calibration-Guided**: Rather than comparing against a baseline in a differential test, we measure the skill's absolute adherence to its design goals using a rubric and a calibration guide.
*   **Regression and Improvement Focus**: The framework helps measure how prompt edits or instruction changes impact the overall pass rate against the rubric.

---

## 2. Assets Architecture

Each skill evaluation is composed of three key parts: a co-located evaluation configuration in the skill folder, centralised test fixtures, and centralised quality rubrics.

### 2.1 Skill-Specific Evaluation Configuration (`eval.md`)
Every skill directory must contain an `eval.md` file. It specifies the assets needed to run the evaluation using YAML frontmatter:

```yaml
---
skill: skills/<platform>/.../<skill-name>/SKILL.md
fixtures: evals/fixtures/<skill-name>.json
rubric: evals/rubrics/<skill-name>.md
---
```

> [!NOTE]
> If the YAML frontmatter is absent, the execution command will fallback to reading the inline fixtures and rubric from the body of the `eval.md` file itself.

The body of the `eval.md` file typically contains:
*   **Simulation Notes**: Contextual details or simulation instructions for the evaluator to execute tests accurately.
*   **Calibration Guide**: Specific instructions on what constitutes a `PASS` or `FAIL` for each rubric criterion.

### 2.2 Centralised Fixtures (`evals/fixtures/`)
All synthetic test scenarios and input files live inside the central [evals/fixtures/](file:///Users/jacob/Projects/skills/evals/fixtures/) folder.
*   **JSON Fixture List**: A single JSON file matching the skill name (e.g. `evals/fixtures/<skill-name>.json`) which defines an array of scenario objects.
*   **Scenario Properties**:
    *   `id`: A unique string identifier for the test case (e.g. `fixture_1_default_no_ticket`).
    *   `description`: A clear summary of the test case objectives.
    *   `input`: The prompt text or scenario description supplied to the skill's sandbox as a user prompt.
    *   `expected_outcome`: A summary of what a successful response looks like.
*   **Directory Fixtures**: For task-oriented skills (like test generation), the `fixtures` path may point to a folder containing mock code or implementation files (e.g., `evals/fixtures/create-tests/`) to be loaded into the sandbox environment.

### 2.3 Centralised Rubrics (`evals/rubrics/`)
All evaluation criteria live inside the central [evals/rubrics/](file:///Users/jacob/Projects/skills/evals/rubrics/) folder.
*   **Structure**: A Markdown file containing clear, observable criteria grouped by category.
*   **Scoring**: For each applicable criterion, the evaluator assigns one of:
    *   **PASS (1)**
    *   **FAIL (0)**
    *   **N/A** (not applicable, excluded from calculation)
*   **Scoring Formula**:
    $$\text{Total Score} = \frac{\sum \text{PASS}}{\sum \text{applicable}} \times 100\%$$

---

## 3. Execution Protocol

The evaluation is executed via the generic `/eval` command defined in [commands/eval.md](file:///Users/jacob/Projects/skills/commands/eval.md). The LLM test runner executes evaluations through four distinct phases:

### Phase 1: Locate the Skill and Assets
1.  Traverse the `skills/` directory to locate the folder matching the requested skill name.
2.  Read the skill's `SKILL.md` (which contains system instructions) and the co-located `eval.md`.
3.  Parse the frontmatter of `eval.md` to load fixtures and rubrics. Fallback to inline assets if frontmatter is absent.

### Phase 2: Execute Fixtures (Simulated Sandbox)
For each loaded fixture:
1.  **Initialise Sandbox**: Isolate the agent environment and load the full contents of `SKILL.md` as the system prompt/instruction set.
2.  **Inject Input**: Pass the fixture's `input` (or loaded file contents) to the sandbox as the user's message.
3.  **Execute**: Generate the raw response exactly as the skill would respond in a production environment, without any evaluator commentary or meta-text.
4.  **Collect**: Store the generated output for grading.

### Phase 3: Rubric Evaluation
For each generated output:
1.  Load the corresponding **Rubric** and **Calibration Guide**.
2.  Inspect the output objectively.
3.  For each criterion in the rubric:
    *   Assess whether the output passes, fails, or if the criterion is not applicable (N/A).
    *   Assign a score of **PASS (1)**, **FAIL (0)**, or **N/A**.
    *   Write a short, precise justification referencing the specific parts of the output that dictated the score.

### Phase 4: Compile & Report
Generate a final evaluation report detailing the results.

---

## 4. Evaluation Report Output

The generated report is written in Markdown format and structured as follows:

### 4.1 Overall Summary Table
A table highlighting the performance of each fixture against the rubric:

| Fixture ID & Description | Criteria Scored | Total Score | Status Rating |
| :--- | :--- | :--- | :--- |
| `fixture_1` - Standard bug fix | 4 / 5 | 80% | Good |
| `fixture_2` - Ticket extraction | 5 / 5 | 100% | Excellent |

> [!TIP]
> **Status Rating Scale**:
> *   **90–100%**: Excellent
> *   **75–89%**: Good
> *   **60–74%**: Needs work
> *   **<60%**: Poor

### 4.2 Detailed Breakdown
A section for each fixture showing the input, expected outcome, actual response, and individual criteria scores with justifications.
```markdown
### Fixture: fixture_1_default_no_ticket
- **Input**: "Branch: main. Changes: modified src/utils.js (fixed off-by-one error)..."
- **Expected Outcome**: Commit type 'fix', subject line under 50 characters...
- **Actual Response**:
  ```
  fix: fix off-by-one error in array index
  
  Would you like me to proceed with this commit message?
  ```
- **Criteria Scores**:
  - `2.1` Correct commit type: **PASS (1)** — Chosen prefix is `fix` for a bug fix.
  - `3.1` Subject ≤50 chars: **PASS (1)** — Subject line is 39 characters.
  - `5.3` Explicit approval question: **PASS (1)** — Explicitly asks "Would you like me to proceed...?"
```

### 4.3 Actionable Recommendations
If the final score is less than 100%, suggestions for concrete edits to the `SKILL.md` prompt to prevent those failure modes.

---

## 5. Analytical & Optimisation Actions

To maintain the high quality of the skills, review the evaluation results and perform the following actions:
*   **Flaky Criteria**: If a criterion passes or fails randomly across identical runs, the skill instructions are too ambiguous. Rewrite them to offer a clear "Why" (reasoning-based direction) rather than just a rigid command.
*   **Dead Criteria**: If a criterion is consistently N/A or always passes without testing a specific capability, review the rubric and either target it with new fixtures or remove/adjust it.
*   **Prompt Tuning**: Actively use the Actionable Recommendations to refine and update the system instructions in `SKILL.md` until the skill consistently achieves an **Excellent** rating across all fixtures.
