# Multi-Agent Code Review Skill

This folder contains the **Multi-Agent Code Review** skill for AI coding assistants. It teaches the agent how to coordinate a feedback loop across seven independent, specialised agents to optimise code quality, enforce security, and validate requirements.

---

## 🏛️ System Design & Filesystem Boundaries

This skill relies on **progressive disclosure** across separate markdown files. Instead of loading all guidelines into the active context at once, you should read these files on-demand:

### 1. Document Schema
*   **[Rules.md](docs/Rules.md)**: Core rules governing code style, security, structure, and DevOps.
*   **[Agent.md](docs/Agent.md)**: Personas, boundaries, and basic specifications for each subagent.
*   **[goal.example.md](docs/goal.example.md)**: Guidelines for writing local optimisation targets.
*   **[Fixture.example.md](docs/Fixture.example.md)**: Specifications for mocking local sandbox test inputs.

### 2. The 7 Specialised Agents
*   **[1-security](agents/1-security.md)**: Security Agent - dedicated to security best practices and vulnerability checks.
*   **[2-best-practices](agents/2-best-practices.md)**: Best Practices Agent - code smell detection, naming standards, and clean code.
*   **[3-structure](agents/3-structure.md)**: Structure Agent - namespace mappings, strict typing, and design pattern compliance.
*   **[4-devops](agents/4-devops.md)**: DevOps Agent - infrastructure settings, container images, and CI/CD pipelines.
*   **[5-business](agents/5-business.md)**: Business Agent - domain logic correctness, calculations, and requirements mapping.
*   **[6-write-design](agents/6-write-design.md)**: Write and Design Agent - generates architectural diagrams (Mermaid) and content flows.
*   **[7-coordinator](agents/7-coordinator.md)**: Coordinator Agent - manages telemetry logs, aggregates scores, and runs loop cycles.

---

## 🔒 Local Sandboxing
To ensure strict isolation, subagents do not interact directly with other agents or the user during analysis. They compile and run their own local tests by creating:
*   `local_goal.md`: Outlines the target goals.
*   `local_fixture.json`: Holds mock input parameters and assertions.
The changes are rated inside this sandbox before being submitted to the Coordinator.

---

## 🧭 Continuous Optimisation Loop

1. **User Prompt**: Initiates the workflow.
2. **Loop Start**:
   *   **Code Change**: The active subagent drafts a code refactoring.
   *   **Eval Result**: The Coordinator evaluates changes against `Rules.md`.
   *   **Suggest Improvement**: Subagents assign score deductions. Total score is calculated as:
       $$\text{Score} = 100 - \sum \text{Deductions}$$
   *   **Apply Result**: Refinements are applied, looping back to draft a new Code Change.
3. **Review Loop**:
   *   The Coordinator reports results, logs, and score trends to the user.
   *   The user chooses to either restart the loop or end it and apply the files.

### 🚨 Telemetry Constraints
*   **Passing Score**: The loop continues until the final score is above the **80%** threshold.
*   **Loop Limit**: The loop is capped at a maximum of **5 cycles** to prevent infinite recursion.
*   **Change History**: Every step logs score changes to show improvement over time.

---

## ⚠️ Gotchas & Common Failure Modes

When executing multi-agent pipelines, watch out for these known issues:
*   **Edit Wars / Conflicting Suggestions**: The Best Practices agent (requesting descriptive naming) might conflict with the DevOps agent (refactoring config properties). The Coordinator must resolve conflicts and strictly enforce the **5-loop limit** to prevent infinite recursion.
*   **Sandbox Pollution**: Ensure agents write goals/fixtures under the temporary run folder (`.cor/runs/<run_id>/`) rather than the workspace root, to avoid leaking files into Git.
*   **Regression of Business Logic**: When refactoring code for DevOps or security, always have the Business Agent verify that no functional business logic or calculation boundaries are broken.

---

## 🧪 Running Evaluations

To run evaluations against this skill locally, execute the slash command in your terminal:

```bash
/eval Antigravity/multi-agent-code-review
```
This runs the synthetic test fixtures and scores the results against the central shared rubric.
