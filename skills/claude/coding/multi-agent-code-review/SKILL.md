---
name: multi-agent-code-review
description: Trigger this skill to run code reviews, check security standards, enforce clean code practices, run multi-agent refactoring, or optimise codebase files using continuous feedback loops.
---

# Multi-Agent Code Review Skill

This skill teaches the agent how to coordinate a multi-agent system of seven specialised agents to review, optimise, and validate code changes through a continuous optimisation loop with local sandboxing.

---

## 🏛️ Context Engineering & Progressive Disclosure

To keep execution contexts clean and efficient, the instructions and boundaries are distributed across specialised sub-files. Read these files on-demand during execution:

### 1. System Documentation & Rules
*   **[Rules.md](docs/Rules.md)**: Core rules governing the entire system.
*   **[Agent.md](docs/Agent.md)**: The base specification for agent behaviours and personas.
*   **[goal.example.md](docs/goal.example.md)**: Intended goals and specifications.
*   **[Fixture.example.md](docs/Fixture.example.md)**: Mock data structures and testing inputs.

### 2. The 7 Independent Agents
*   **[1-security.md](agents/1-security.md)**: Security Agent - dedicated to security best practices.
*   **[2-best-practices.md](agents/2-best-practices.md)**: Best Practices Agent - quality and standards.
*   **[3-structure.md](agents/3-structure.md)**: Structure Agent - architecture and organisation.
*   **[4-devops.md](agents/4-devops.md)**: DevOps Agent - infrastructure and environment.
*   **[5-business.md](agents/5-business.md)**: Business Agent - domain logic and requirements.
*   **[6-write-design.md](agents/6-write-design.md)**: Write and Design Agent - generates content and blueprints.
*   **[7-coordinator.md](agents/7-coordinator.md)**: Coordinator Agent - orchestrates loop flow and scoring.

---

## 🧭 Continuous Optimisation Loop Protocol

When a code review task is initiated, the Coordinator agent executes the following loop:

### Phase 1: Local Sandboxing
Before proposing any changes to the user or other agents, each active agent must compile its own local mock test inputs and expectations:
1. Write the agent's target goals to `local_goal.md`.
2. Write the mock test cases to `local_fixture.json`.
3. Execute the code changes against the local sandbox to calculate the initial deduction score.

### Phase 2: Optimisation Loop
1. **Loop Start**:
   *   **Code Change**: The designated agent generates a code modification based on the prompt.
   *   **Eval Result**: The change is automatically evaluated against the rules.
   *   **Suggest Improvement**: Refinements are suggested based on metric deductions.
   *   **Apply Result**: Apply the suggestions and feed them back into a new Code Change step.
2. **Scoring & Constraints**:
   *   **Passing Score**: The deduction score must be optimised to keep the final passing score above **80%**.
   *   **Loop Limit**: The loop is capped at a maximum of **5 cycles**. If stuck, halt and report.
   *   **Change History**: Log the score trends and change history over time.

### Phase 3: Review Loop
1. Report final score, modifications made, and sandbox status.
2. Prompt the user to either restart the loop or end the loop and finalise changes.

---

## ⚠️ Gotchas & Common Failure Modes

When executing multi-agent pipelines, watch out for these known issues:
*   **Edit Wars / Conflicting Suggestions**: The Best Practices agent (requesting descriptive naming) might conflict with the DevOps agent (refactoring config properties). The Coordinator must resolve conflicts and strictly enforce the **5-loop limit** to prevent infinite recursion.
*   **Sandbox Pollution**: Ensure agents write goals/fixtures under the temporary run folder (`.cor/runs/<run_id>/`) rather than the workspace root, to avoid leaking files into Git.
*   **Regression of Business Logic**: When refactoring code for DevOps or security, always have the Business Agent verify that no functional business logic or calculation boundaries are broken.

