---
name: review-commit
description: Use when you have uncommitted git changes and want to commit them with a properly formatted message. Scans all staged and unstaged changes, generates a [Conventional Commits](../../../../docs/commit-message.md) message with the ticket scope extracted according to user configuration (e.g. from the branch name or worked out from changes), flags sensitive files (.env, keys, credentials), and waits for explicit approval before staging or committing anything.
---

# Review and Commit Git Changes

Analyse all git changes, generate a [conventional commit](../../../../docs/commit-message.md) message, and present it for user review before committing.

**Usage**: `/review-commit`

## Steps to perform:

1. **Check for changes and load/setup configuration**:
   - Run `git status --porcelain` to check for any changes
   - If no changes exist, inform the user and stop
   - Check if a configuration file named `commit-message.json` or `.review-commit.json` exists in the workspace root.
   - If not found, use the `AskUserQuestion` tool to interactively prompt the user: "Would you like to automatically extract ticket IDs from your git branch names to use as the commit scope?"
     - Option 1: "Yes, automatically extract ticket IDs from branch names" (Sets `extractTicketFromBranch: true`)
     - Option 2: "No, leave scope blank by default unless found in changes" (Sets `extractTicketFromBranch: false`)
     - Save the user's choice along with `"allowScopeFromChanges": true` as a JSON configuration to `commit-message.json` at the workspace root.
   - Load the configuration from the workspace root (or fallback to the skill directory's default `config.json`).
   - Proceed to step 2

2. **Analyse all changes in parallel**:
   - Run `git status` to see all tracked/untracked files
   - Run `git diff` to see all unstaged changes
   - Run `git diff --staged` to see all staged changes
   - Run `git log --oneline -10` to see recent commit messages for style reference
   - From the full file list, identify any **sensitive paths** — match on filename/extension only, not directory components: `.env`, `.env.local`, `.env.production`, `.env.staging`, `.env.development` (do NOT flag `.env.example`, `.env.dist`, `.env.sample`, or other committed templates), `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.token`, `*.keystore`, `*_rsa`, `*_dsa`, `*_ecdsa`, `*_ed25519`, `credentials.json`, `auth.json`, `secrets.json`, `service-account.json`. Do NOT flag files whose names merely contain words like "password", "secret", or "credentials" — those patterns match legitimate source files (e.g. `PasswordResetHandler.php`).
   - **If every changed file is sensitive** (no safe files remain), show the warning block listing all flagged files, tell the user there is nothing safe to commit, and **stop immediately** — do not proceed to step 3 or beyond.

3. **Draft commit message using [Conventional Commits](../../../../docs/commit-message.md) format**:
   - Read and follow the guidelines in the global commit message guide [docs/commit-message.md](../../../../docs/commit-message.md). If the global guide contains customised types, length limits, or casing standards, follow those instructions. Otherwise, use the standard guidelines below.
   - Analyse all the changes (both staged and unstaged)
   - Choose the appropriate type prefix:
     - `feat` — introduces a new feature, including filling in a stub or placeholder with real behaviour
     - `fix` — fixes a bug
     - `refactor` — restructures existing working code without changing behaviour or fixing a bug; do NOT use if a previously unimplemented stub is now given real logic
     - `chore` — miscellaneous changes that don't touch src or test files (e.g. deps, .gitignore)
     - `perf` — improves performance
     - `ci` — changes to CI/CD configuration or pipelines
     - `ops` — changes to infrastructure, deployment, backup, or recovery
     - `build` — changes to build system, build tools, or project version
     - `docs` — documentation-only changes
     - `style` — formatting, whitespace, missing semicolons — no logic changes
     - `revert` — reverts a previous commit
     - `test` — adds missing tests or corrects existing tests
   - Determine the scope (ticket ID):
     - If `extractTicketFromBranch` is `true`, check the current branch name for a ticket pattern matching `[A-Z]+-\d+` (e.g. `feature/HVS-10_...` → `HVS-10`) and use it as the scope.
     - If `extractTicketFromBranch` is `false` (default), do NOT use the branch name. Only set the scope if `allowScopeFromChanges` is `true` AND a ticket ID (matching `[A-Z]+-\d+`) can be worked out from the changes (e.g., in modified file content, comments, or recent commit logs).
     - Otherwise, omit the scope and parentheses entirely: `type: Subject`.
   - Format:
     ```
     type(TICKET-ID): Capitalised short title here

     Body lines explaining what and why, wrapped at 72 characters.
     Use bullet points for individual changes:
     - First specific change
     - Second specific change
     ```
   - Subject line rules:
     - Must be 50 characters or fewer (including the `type(scope): ` prefix) — count every character before drafting; shorten with abbreviations (e.g. "in" instead of "inside", drop articles) rather than truncating mid-word. Aim for ≤45 chars as a safety margin — the `type(scope): ` prefix alone can consume 16+ chars on longer ticket IDs, leaving little room
     - First word after the colon must be capitalised
     - Must NOT end with a period
     - Use imperative mood ("Add unit tests" not "Added unit tests")
   - Body rules:
     - Separated from subject by a blank line
     - Each line wrapped at 72 characters
     - Explains what changed and why (not how) — include the business reason or failure scenario the change addresses; "why" means the real-world context (e.g. "free orders have no payment, previously caused a crash"), not a restatement of the code change. For security-sensitive changes, name the threat being mitigated (e.g. "prevents unauthenticated actors from triggering payment events")
   - Footer and Breaking Change rules (conforming to Conventional Commits v1.0.0):
     - A breaking change must be indicated by appending an exclamation mark `!` after the type/scope (e.g. `feat(auth)!:` or `feat!:`) and/or including a `BREAKING CHANGE: <description>` footer.
     - Footers must appear at the very end of the message, separated from the body by a blank line. Each footer must follow the structure: `<token>: <value>` or `<token> #<value>` (e.g., `Refs #123` or `Reviewed-by: Name`).

4. **Present for review**:
   - Show the user:
     - Summary of files changed
     - Sensitive path scan result — always state this explicitly: either a **warning block** listing each flagged file and stating it will be excluded, or a single line confirming no sensitive files were detected (e.g. "Sensitive path scan: no files flagged"). Do NOT proceed until the user acknowledges if files were flagged.
     - The proposed commit message
   - Explicitly ask: "Would you like me to proceed with this commit message, or would you like to modify it?"
   - **IMPORTANT**: Do NOT proceed with the commit until the user explicitly approves

5. **Commit changes (only after user approval)**:
   - If **no** sensitive paths were identified: `git add -A`
   - If sensitive paths **were** identified: stage only the safe files individually by name — never use `git add -A` when sensitive paths are present
   - Create the commit with the approved message
   - Run `git status` to confirm the commit was successful
   - Append the approved commit message, branch name, and timestamp to an append-only log file `commits.log` at the workspace root to serve as a persistent history and style reference for future commits.

## Important Notes:

- **Never commit without explicit user approval**
- Sensitive paths (`.env`, keys, credentials, tokens, etc.) are always excluded from the commit — flag them in the summary and never stage them
- If user wants to modify the message, update it and ask for approval again
- All non-sensitive changes (staged and unstaged) will be included in the commit
- If no ticket ID is configured to be extracted or can be worked out from the changes, omit the scope entirely: `type: Subject`

## Gotchas

**Sensitive path detection is filename-only, not path-based.**
Match on the file's name and extension alone — not on directory components. `src/Auth/PasswordResetHandler.php` is safe; `.env.production` is not. Do NOT flag files that merely contain the words "password", "secret", or "credentials" in their name — those are legitimate source files. Only flag the exact patterns listed in step 2.

**`.env.example`, `.env.dist`, `.env.sample` are NOT sensitive.**
These are committed templates. Flag only actual env files: `.env`, `.env.local`, `.env.production`, `.env.staging`, `.env.development`.

**All-sensitive early exit happens at step 2, not step 5.**
If every changed file is sensitive, output the warning block and stop immediately — do not draft a commit message, do not ask for approval, do not proceed.

**Scope extraction and config constraints.**
Always respect `extractTicketFromBranch` (default `false`) and `allowScopeFromChanges` (default `true`). When extracting the ticket ID (whether from the branch name or worked out from changes), extract only the `[A-Z]+-\d+` portion (e.g., from `feature/HVI-123_add_payment` scope is `HVI-123`). If no ticket ID is extracted or worked out, omit the scope and parentheses entirely: `type: Subject`.

**`refactor` vs `feat`: filling in a stub counts as `feat`.**
If a previously unimplemented method or class stub is given real logic, that is a new feature (`feat`), not a restructure (`refactor`). Use `refactor` only when existing working behaviour is restructured without changing what it does.

**Subject line budget is tight — count including the prefix.**
`type(TICKET-ID): ` alone can consume 16+ characters on longer ticket IDs. The full subject must be ≤50 characters. Aim for ≤45 as a safety margin; abbreviate ("in" not "inside", drop articles) rather than truncating mid-word.

**Body "why" means real-world context, not code description.**
"Adds null check before calling refund()" is a what, not a why. "Free orders have no payment intent — previously caused a crash on cancellation" is a why. For security changes, name the threat mitigated.

## Example workflow:

```
User: /review-commit

Claude: I've analysed your changes. Here's what I found:

Files changed:
- src/Dashboard/Handler/SettingsHandler.php (modified)
- src/Dashboard/Views/Forms/SettingsForm.php (new file)
- tests/Unit/Dashboard/Handler/SettingsHandlerTest.php (modified)

Proposed commit message:
refactor(DASH-123): Use DashboardForm in settings

- Replace legacy ZF1 form with DashboardForm pattern
- Add TransferModel for type safety

Would you like me to proceed with this commit message, or would you like to modify it?

User: Looks good, proceed

Claude: [Commits the changes with the approved message]
```
