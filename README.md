# Skills

A specialised repository of modular skills, commands, and automation scripts crafted in Markdown to inject robust domain knowledge, behavioural rules, and specific technical capabilities directly into AI coding assistants (like Antigravity, Claude CLI, or custom LLM agents).

---

## 🧩 What is an "AI Skill"?

In modern development, treating Markdown context as infrastructure allows us to build predictable, high-performing AI workflows. Each `.md` file in this repository acts as a "skill block" or system prompt that teaches an LLM exactly how to behave, write code, or execute tasks within a specific domain.

---

## 🧭 Evaluation Harness (`evals/` and `/eval`)

To maintain the quality of these prompt-only artifacts, this repository includes a self-scoring evaluation framework:
- **Centralised Evals**: All synthetic test fixtures and rubrics live inside the central [evals/](file:///Users/jacob/Projects/skills/evals/) folder.
- **Co-located Eval References**: Each skill subdirectory contains an `eval.md` which uses frontmatter to declare its corresponding central fixtures and rubrics.
- **Slash Command**: A single generic command defined in [commands/eval.md](file:///Users/jacob/Projects/skills/commands/eval.md) allows running evaluations programmatically or interactively via `/eval <skill-name>`.

---

## 📂 Repository Structure

```text
├── commands/
│   └── eval.md             # The generic /eval command definition
├── evals/
│   ├── fixtures/           # Synthetic test inputs/code for all skills
│   └── rubrics/            # Quality assessment rubrics for evaluation
├── skills/
│   ├── Antigravity/        # Skill definitions formatted for Antigravity
│   ├── Claude CLI/         # Skill definitions formatted for Claude CLI
│   ├── Custom harness/     # Skill definitions for custom harnesses
│   └── SLM                 # Skill definitions optimised for Small Language Models (SLMs)
└── README.md               # Project documentation
```
