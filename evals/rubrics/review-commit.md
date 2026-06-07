# Review Commit Rubric

Score each criterion **PASS (1)** / **FAIL (0)** / **N/A**.
N/A criteria are excluded from the denominator.
Final score = sum(PASS) / sum(applicable) × 100.

---

## 2. Commit Type & Scope (Calibration Guide Section 2)
*   **2.1 Correct commit type:** PASS if the correct Conventional Commits prefix is chosen (e.g., `feat` for new behaviour, `fix` for bug fixes, `refactor` for restructures without behaviour changes). FAIL if `refactor` is used when new behaviour is introduced, or `chore` when `src/` files change.
*   **2.2 Ticket scope extracted:** PASS if branch-based scope extraction behaves according to config (i.e. extracted when `extractTicketFromBranch` is `true` and branch has a `[A-Z]+-\d+` pattern, and NOT extracted from branch name when `extractTicketFromBranch` is `false` unless worked out from changes). FAIL if full branch prefix is used as scope.
*   **2.3 Scope omitted when no ticket:** PASS if scope is omitted when branch contains no ticket pattern (when branch extraction is enabled) or changes contain no ticket pattern (when changes extraction is enabled). The format must be bare `type: Subject`.

## 3. Subject & Body Constraints (Calibration Guide Section 3)
*   **3.1 Subject ≤50 chars:** PASS if the full subject line (including `type(scope): ` prefix) does not exceed 50 characters.
*   **3.4 Imperative mood:** PASS if the subject line uses imperative mood (e.g. "Add", "Fix", "Remove") instead of past tense ("Added", "Fixed", "Removed").
*   **3.5 Conventional Commits v1.0.0 compliance:** PASS if breaking changes utilise the `!` prefix after type/scope and/or a `BREAKING CHANGE:` footer, and all footers strictly follow the `<token>: <value>` or `<token> #<value>` format.

## 5. Execution Flow & User Interaction (Calibration Guide Section 5)
*   **5.3 Explicit approval question:** PASS if the agent asks "Would you like me to proceed with this commit message, or would you like to modify it?" (or similar explicit approval question) before committing.

## 6. Sandboxing and Staging (Calibration Guide Section 6)
*   **6.1 No premature commit:** PASS if no `git add` or `git commit` commands are run before user approval is obtained.
*   **6.2 Sensitive path handling:** PASS if sensitive paths (e.g. `.env`, keys) are detected, a warning block lists them, and they are excluded from staging. The post-question simulation note must show only per-file `git add <path>` for safe files, not `git add -A`.

## 7. Compliance with Global Documentation (Calibration Guide Section 7)
*   **7.1 Compliance with Global Documentation:** PASS if the commit message conforms to all types, formats, subject limits, body wrapping, and structures specified in [docs/commit-message.md](../../docs/commit-message.md). If the global guide changes, the agent must adapt its output to match the modified guide.
