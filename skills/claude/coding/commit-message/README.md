# review-commit

Analyse all git changes, generate a [Conventional Commits](../../../../docs/commit-message.md) message, and wait for explicit approval before staging or committing anything.


## What it does

- Derives scope from the current branch name (e.g. `feature/HVI-10_...` → `HVI-10`)
- Flags sensitive files (`.env`, keys, credentials) and excludes them automatically
- Never commits without explicit user approval

## Usage

```
/review-commit
```

## Related files

- [SKILL.md](SKILL.md) — full skill instructions

