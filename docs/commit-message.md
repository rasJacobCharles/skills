# How to Write a Commit Message

This guide documents the standards and best practices for writing high-quality commit messages across our projects. It strictly conforms to the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification.

---

## 🏗️ Structure of a Commit Message

A commit message consists of a **Header**, a **Body** (optional but recommended for non-trivial changes), and a **Footer** (optional).

```
<type>(<scope>): <subject>

<body>

<footer>
```

---

## 1. The Header

The header is the most important part of the commit message. It must be concise and follow a strict format.

### Type
The type prefix describes the nature of the change. Use one of the following standard types:

| Type | Description | Example |
| :--- | :--- | :--- |
| `feat` | A new feature (includes implementing a previously empty stub or placeholder) | `feat(auth): add MFA support` |
| `fix` | A bug fix | `fix(billing): correct tax calculation for UK orders` |
| `refactor` | Restructuring existing working code without changing behaviour or fixing a bug | `refactor(db): optimise query builder instantiation` |
| `chore` | Miscellaneous changes that don't modify source or test files (e.g., dependencies, configuration) | `chore(deps): upgrade lodash to 4.17.21` |
| `perf` | A code change that improves performance | `perf(parser): reduce AST traversal overhead` |
| `ci` | Changes to CI/CD configuration files and scripts | `ci(github): add matrix build for node versions` |
| `ops` | Changes to infrastructure, deployment, backup, or recovery | `ops(k8s): increase replica count for API service` |
| `build` | Changes that affect the build system, build tools, or project versions | `build(npm): update lockfile structure` |
| `docs` | Documentation-only changes | `docs(readme): document environment variables` |
| `style` | Code style changes (formatting, missing semicolons, etc. with no logic changes) | `style(lint): fix indentation in user controller` |
| `test` | Adding missing tests or correcting existing tests | `test(auth): add unit test for token expiry` |
| `revert` | Reverting a previous commit | `revert: feat(auth): add MFA support` |

### Scope (Ticket ID)
The scope is optional but highly recommended. It must be enclosed in parentheses immediately after the type.
*   **Ticket ID**: Use the exact Ticket ID/Issue ID from your project management system (e.g., `HVS-123`, `DASH-45`).
*   **Derivation & Configuration**:
    When using automated tooling (like the `review-commit` skill), scope derivation is determined by a workspace-level configuration file (`commit-message.json` or `.review-commit.json`):
    - `extractTicketFromBranch` (default: `false`): If `true`, the ticket ID is extracted from the active branch name (e.g., `feature/HVS-123_setup-auth` -> `HVS-123`).
    - `allowScopeFromChanges` (default: `true`): If `true`, the tool attempts to work out a ticket ID from the modified file names, comments, or commit history if not pulling from the branch name.
    - If neither applies, or if no ticket ID is resolved, the scope is omitted entirely (e.g., `feat: Subject`).

### Breaking Change Indicator (`!`)
A breaking change can be indicated in the header by appending an exclamation mark `!` immediately after the type or scope, and before the colon (e.g., `feat!: upgrade runtime version` or `feat(auth)!: replace legacy hashing`). This signals a breaking change and must be accompanied by a `BREAKING CHANGE:` entry in the footer.

### Subject
The subject is a short summary of the code changes:
*   **Length**: Must be **50 characters or fewer** (including the `type(scope): ` prefix).
*   **Capitalisation**: The first word after the colon must start with a capital letter.
*   **Punctuation**: Do **not** end the subject line with a period.
*   **Mood**: Use the **imperative mood** (e.g., "Add feature" instead of "Added feature" or "Adds feature"). Think of it as completing the sentence: *"If applied, this commit will..."*

---

## 2. The Body

The body provides additional context for the commit. It is separated from the header by a single blank line.

*   **Wrapping**: Wrap lines at **72 characters** to ensure readability in terminal logs.
*   **Focus**: Explain **what** changed and **why** (the business reason or failure scenario), not *how* (the code itself shows *how*).
*   **Real-World Context**: Provide the real-world impact (e.g., *"Free orders have no payment intent, which previously caused a null pointer crash on cancellation"*).
*   **Security Changes**: For security-sensitive modifications, explicitly state the threat being mitigated (e.g., *"Prevents unauthenticated actors from triggering payment events"*).

---

## 3. The Footer

One or more footers may be provided after the body, separated by blank lines. Each footer must consist of a word token, followed by either a `:<space>` or `<space>#` separator, followed by a value (e.g., `BREAKING CHANGE: Description` or `Refs #123`).

*   **Breaking Changes**: A breaking change must be introduced as a footer starting with the uppercase text `BREAKING CHANGE:` followed by a space and a description of the breaking change/migration path.
*   **Footer Tokens**: Other footers must use a word token (using `-` in place of whitespace, e.g., `Reviewed-by: Name`) or ticket indicators (e.g., `Closes #45`).

---

## 📝 Examples

### Feature with Scope
```
feat(AUTH-89): Add password strength validation

- Enforce minimum length of 12 characters
- Require at least one uppercase letter, number, and special character
```

### Bug Fix without Scope
```
fix: Prevent null pointer on missing user profile

Ensure profile object is initialised before reading attributes to avoid
crashes when loading new user accounts.
```

### Breaking Change
```
feat(API-12)!: Remove v1 endpoints

BREAKING CHANGE: The /v1/users endpoint is now removed. Users must migrate
to /v2/users, which returns the standardised payload structure.
```
