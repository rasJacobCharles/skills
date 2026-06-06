# Multi-Agent Code Review Rubric

Score each criterion **PASS (1)** / **FAIL (0)** / **N/A**.
N/A criteria are excluded from the denominator.
Final score = sum(PASS) / sum(applicable) × 100.

---

## 1. Agent Specialisation (C1)
*   **1.1** All seven specialised agents are defined (Security, Best Practices, Structure, DevOps, Business, Write and Design, and Coordinator). (verify via agent files)
*   **1.2** Each agent maintains isolated boundaries and specific objectives. (verify via agent descriptions)
*   **1.3** The Coordinator Agent orchestrates loops and manages termination constraints. (verify via instructions)

## 2. Documentation Compliance (C2)
*   **2.1** `Rules.md` defines system-wide rules and guidelines. (verify via file exist/content)
*   **2.2** `Agent.md` details base instruction schemas for agent personas. (verify via file exist/content)
*   **2.3** `goal.example.md` and `Fixture.example.md` provide clear mock examples. (verify via file exist/content)

## 3. Continuous Optimisation Loop (C3)
*   **3.1** Pipeline executes a loop of Code Change ➔ Eval Result ➔ Suggest Improvement ➔ Apply Result. (verify via protocol logs)
*   **3.2** Outcomes are reported to the user with restart/end options at the end of the review loop. (verify via logs)
*   **3.3** The system logs a change history tracking score trends over time. (verify via history log)

## 4. Scoring & Constraints (C4)
*   **4.1** Optimisation targets a passing score above 80% based on score deductions. (verify via log)
*   **4.2** Execution halts immediately with a loop limit warning if the loop repeats 5 times without resolution. (verify via log)

## 5. Local Sandboxing (C5)
*   **5.1** Agents compile and execute local, sandboxed versions of goals and fixtures on disk to rate suggestions prior to interaction. (verify via logs)
