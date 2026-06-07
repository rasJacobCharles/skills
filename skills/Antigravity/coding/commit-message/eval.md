---
skill: skills/Antigravity/coding/commit-message/SKILL.md
fixtures: evals/fixtures/review-commit.json
rubric: evals/rubrics/review-commit.md
---

## Simulation note

After the approval question, add a clearly labelled simulation note declaring the step 5 staging commands you *would* run on approval — e.g. `*(On approval: git add -A)*` or `*(On approval: git add <file>)*`. This note is a simulation artifact only; it must appear **after** the approval question, never before. It is required for rubric criterion 6.2 to be scoreable and is exempt from rubric criterion 6.1's pre-approval check.

## Calibration guide

**2.1 Correct commit type**: FAIL if `refactor` is used when new behaviour is introduced (should be `feat`), or `chore` when `src/` files change.

**2.2 Ticket scope extracted**: FAIL if scope is extracted from the branch name when `extractTicketFromBranch` is `false` (unless it is worked out from changes and `allowScopeFromChanges` is `true`), or if scope is omitted when `extractTicketFromBranch` is `true` and the branch contains a `[A-Z]+-\d+` pattern. FAIL if the full branch prefix is used as the scope (e.g. `feature/HVI-123` instead of `HVI-123`).

**2.3 Scope omitted when no ticket**: FAIL if a scope is invented or guessed when no ticket pattern is found in the branch name (when branch extraction is enabled) or changes (when changes extraction is enabled). The format must be bare `type: Subject`.

**3.1 Subject ≤50 chars**: FAIL if the full subject line (including `type(scope): ` prefix) exceeds 50 characters. Count every character.

**3.4 Imperative mood**: FAIL if past tense is used ("Added", "Fixed", "Removed"). Must read as a command.

**3.5 Conventional Commits v1.0.0 compliance**: FAIL if breaking changes do not use the `!` prefix after type/scope and/or a `BREAKING CHANGE:` footer, or if footers violate the `<token>: <value>` or `<token> #<value>` syntax.

**5.3 Explicit approval question**: FAIL if the output commits without first showing the message and asking "Would you like me to proceed?" The question must be present — not implied.

**6.1 No premature commit**: FAIL if `git add` or `git commit` appears *before* the approval question. Everything before that question must be limited to the file summary, scan result line, warning block (if any), and commit message draft. The post-question simulation note is exempt — it appears after the approval question by definition.

**6.2 Sensitive path handling (scenario 4)**: Score the post-question simulation note. FAIL if `git add -A` appears in that note when sensitive paths were detected — only per-file `git add <path>` for the safe files is acceptable. FAIL if no warning block appeared before the approval question.

**7.1 Compliance with Global Documentation**: FAIL if the generated commit message does not conform to the types, limits, or structure rules specified in [docs/commit-message.md](../../../../docs/commit-message.md). If the global guide changes, the agent must dynamically adapt its commit output to match those changes.
