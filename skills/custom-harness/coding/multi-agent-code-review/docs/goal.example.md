# Goal Example: User Hashing Optimisation

This file serves as a guide for agents to write their local optimisation goals.

---

## 🎯 Target Criteria

1.  **Security**: Convert obsolete MD5 hashing functions to secure password hashing.
2.  **Readability**: Rename short variable names (`$u`, `$p`) to clear descriptive alternatives (`$username`, `$password`).
3.  **Strict Typing**: Ensure file includes `declare(strict_types=1);`.

---

## 📉 Expected Deductions
*   Use of `md5()`: -20 points.
*   Single-letter variables: -10 points.
*   Missing strict types: -10 points.
*   **Total Initial Deduction**: -40 points (Initial Score: 60%).
*   **Goal**: Reduce deductions to 0 points (100% Score).
