# The AI Skill Architecture Blueprint
A "Skill" is not just a markdown prompt. A Skill is a modular, context-isolated directory containing natural language guardrails, scripts, static data assets, and dynamic configuration hooks designed for an AI agent to discover, explore, and execute.

##I. Structural Standards (Progressive Disclosure)
Do not dump all knowledge into a single prompt file. This bloats the LLM's context window with irrelevant data, degrades attention, and costs more. Use the file system to implement Progressive Disclosure—give the agent a top-level map, and let it fetch deep context only when needed.

###Standard Directory Structure
```text
my-agent-skill/
├── skill.json          # Meta-description for the agent's global discovery phase
├── SKILL.md            # Master orchestrator: Core intent, high-level map, and gotchas
├── config.json         # Dynamic, user-specific or environment configuration
├── scripts/            # Executable automation, verification drivers, or API wrappers
│   └── verify.sh
├── assets/             # Checklists, response templates, schemas
│   └── output-template.md
└── reference/          # Granular deep-dives (read by agent only when needed)
    ├── api-signatures.md
    └── edge-cases.md
```
    
###1. The Discovery Layer (skill.json / Top-level description)
Rule: Write descriptions explicitly for the model, not for humans.
Rule: Maximise keyword density and define exact trigger boundaries. When the agent initialises a session, it scans this index to decide: "Does a skill exist for the user's request?"
Bad: "Helps you with the database."
Good: "Use this skill when modifying, querying, or troubleshooting the append-only Subscriptions Postgres table. Contains schema gotchas and data-fetching utilities."
###2. The Master Layer (SKILL.md)
This acts as the agent's mental anchor. It must point to the rest of the file system so the agent knows what to look up.
Rule: Tell the agent what other files exist in the directory and when to open them.
Example: "If a deployment job becomes stuck or pending, immediately open and read reference/stuck-jobs.md to diagnose the state before taking destructive action."

##II. The Nine Core Skill Archetypes
To prevent "skill bloat" and agent confusion, every skill must fit cleanly into exactly one of these nine archetypes. If a skill straddles multiple categories, break it apart.

| Archetype | Core Purpose | Best Practice / Implementation |
| :--- | :--- | :--- |
| 1. Library & API Reference | Explains how to correctly use an internal/stubborn SDK or CLI. | Bundle a folder of reference code snippets and a hard list of syntax footguns. |
| 2. Product Verification | Drives external tools to prove code/changes actually work. | Highest ROI archetype. Include testing scripts (e.g., Playwright/tmux drivers) and force state assertions. |
| 3. Data Fetching & Analysis | Connects to monitoring, logging, and metrics stacks. | Provide specific datasource UIDs, canonical table joins, and log field mappings. |
| 4. Process Automation | Collates scattered inputs into a unified output. | Write simple instructions, but have the agent log results to a file to maintain state. |
| 5. Code Scaffolding | Generates framework boilerplates with native guardrails. | Use when code gen requires natural language context that basic CLI tools lack. |
| 6. Code Quality & Review | Enforces organizational standards and stylistic alignment. | Run these via agent hooks or CI/CD pipelines; use deterministic linters alongside the LLM. |
| 7. CI/CD & Deployment | Handles fetching, pushing, rolling out, or rolling back code. | Include strict step-by-step verification before progressing traffic. |
| 8. Runbooks | Maps an error symptom to a multi-tool investigation path. | Accept an error log or alert as input, then output a highly structured diagnostic report. |
| 9. Infra Operations | Performs routine maintenance and critical/destructive changes. | Bake in mandatory "soak periods" and hard user-confirmation gates. |

##III. Writing & Prompting Engineering Principles
1. Never State the Obvious
The LLM already knows standard programming patterns, language syntax, and how to read a file structure.
Rule: Do not write skills that restate default behaviours. Focus exclusively on idiosyncratic knowledge—the things unique to your system that push the model out of its generic training data.
2. Build a Mandatory "Gotchas" Section
The highest-signal content in any skill is a compilation of past failures. Whenever an agent (or human) fails at a task, document the exact structural reason in the skill.
Rule: Use explicit, concrete mappings. Do not use abstract warnings.
Bad: "Be careful when querying user IDs across different microservices."
Good (Gotcha Style):
The subscriptions table is append-only. The target row is always the one with the highest version, not the most recent created_at.
This identifier is labelled @request_id in the API gateway, but named trace_id in the billing service. They hold the exact same value.
3. Avoid "Railroading" the Agent
Rule: Provide absolute constraints on outcomes, but grant flexibility on execution paths.
If instructions are too rigid or overly prescriptive, the agent will break or halt when encountering minor real-world variations (e.g., a network hiccup or an updated CLI flag). Tell the agent what the final state must look like, and let it adapt dynamically to environmental feedback.
4. Interactive Configuration and State Management
Skills often require runtime environment details (API keys, specific Slack channel IDs, target deployment environments).
Rule: Store local execution context in a localised config.json.
Rule: Instruct the agent to check config.json immediately upon activation. If parameters are missing, it must proactively prompt the user for input using an interactive tool (like AskUserQuestion) and save those responses back to config.json for future sessions.
IV. Design Checklist for New Skills
Before deploying a new skill to your AI harness, run it through this validation rubric:
- Is it isolated? Does it focus on exactly one of the 9 archetypes?
- Is it searchable? Is the skill.json or discovery prompt optimised with dense keywords targeted at the agent's router?
- Is it light? Have long reference logs or heavy API schemas been broken out into separate files for progressive disclosure?
- Is it deterministic where possible? Are tedious tasks offloaded to executable scripts inside the skill's /scripts directory rather than relying purely on LLM prompting?
- Does it verify its work? Does it contain an explicit verification step or script to assert that its output is functional?

