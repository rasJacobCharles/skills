# System Rules & Guidelines

These rules govern the entire Multi-Agent Code Review system. Every modification must be evaluated against these constraints, and violations will result in score deductions.

---

## 🎯 1. Security Rules
*   **SEC-01**: Sensitive data must not be logged or exposed in plaintext.
*   **SEC-02**: Inputs must be validated and sanitized/parameterized to prevent injection attacks (SQLi, XSS).
*   **SEC-03**: Cryptographic operations must use industry-standard algorithms (e.g. `password_hash`, `bcrypt`). Never use MD5 or SHA1 for passwords.

## 🏆 2. Best Practices Rules
*   **BP-01**: Variables, classes, and methods must use descriptive names. No single-letter variables except loop iterators.
*   **BP-02**: Functions must be small and focused on a single responsibility.
*   **BP-03**: Code must include docstrings and basic inline comments.

## 🏗️ 3. Structure & Architecture Rules
*   **STR-01**: The system must adhere to modular design patterns (e.g., MVC, CoR, Clean Architecture).
*   **STR-02**: Test files must mirror source code directories under the `Tests` namespace.
*   **STR-03**: All classes must have declared strict types (`declare(strict_types=1);`).

## 🛠️ 4. DevOps & Environment Rules
*   **DEV-01**: Configuration keys, passwords, and secrets must be loaded from environment variables (e.g., `.env`), never hardcoded.
*   **DEV-02**: Container deployment files (e.g. `Dockerfile`) must use explicit base tags (not `latest`).
