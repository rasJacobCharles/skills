# Agentic Chain of Responsibility (CoR) Workflow Skill

This folder contains the **Chain of Responsibility (CoR)** workflow skill for AI coding assistants. It teaches the agent how to execute complex, multi-stage task pipelines by passing a **Shared Context** file along a sequence of decoupled, single-responsibility check handlers.

---

## 🏛️ Design Philosophies

This skill is designed as a template for building robust agentic systems using two key design paradigms:

### 1. Context Engineering (Filesystem-based State)
Instead of forcing the agent to retain the entire execution memory in active context (which is volatile and prone to decay over long tasks), the **Shared Context** is saved directly on disk as a persistent JSON file (`.cor/runs/<run_id>/context.json`). Each handler in the chain reads this file, performs its checks or mutations, and saves the updated state back to disk before forwarding to the next link.

### 2. Progressive Disclosure (Linked Instructions)
To keep the agent's active context window compact, clean, and focused, the instructions are split across modular files. The agent loads the main `SKILL.md` first and dynamically resolves details on-demand by following relative file paths (e.g. loading schema validations or loop detector guardrails only when executing those phases).

---

## 📂 Folder Structure

```text
chain-of-responsibility/
├── README.md                 # This human-readable guide
├── SKILL.md                  # Main router and pipeline execution protocol
├── eval.md                   # Evaluation mappings (points to central fixtures & rubrics)
├── schema/
│   └── context_schema.json   # JSON Schema specifying the Shared Context memory format
├── handlers/
│   ├── base_handler.md       # Template and instructions on how to write custom handlers
│   ├── loop_detector.md      # Loop check guardrails (abort if handler run count > 3)
│   └── fallback_handler.md   # Safety route triggered upon unconsumed payloads/errors
└── examples/
    ├── README.md             # Index of example pipelines
    ├── clean_text_pipeline/  # Text cleaning pipeline setup
    │   ├── pipeline.yaml     # Configures order: CleanTextHandler -> ProfanityFilterHandler
    │   └── context.json      # Shared context state log
    └── code_review_pipeline/ # Code review pipeline setup
        ├── pipeline.yaml     # Configures order: SyntaxCheck -> StaticAnalysis -> MockCheck
        └── context.json      # Shared context state log
```

---

## 🧭 How the Chain Runs (Execution Protocol)

1. **Ingress**: The client requests execution, specifying a task, input data, and a target `pipeline.yaml`.
2. **Context Creation**: The agent creates the initial `context.json` file on disk under `.cor/runs/<run_id>/`.
3. **Traversal Loop**:
   *   Look up the active handler defined in `pipeline.yaml`.
   *   Read the handler's markdown instructions from `.cor/pipelines/<pipeline_name>/handlers/`.
   *   Perform the transformations/validations on the payload.
   *   Increment the handler's execution count. If the count reaches **3**, trigger a `LoopException` and halt.
   *   Append the operation to the log and save changes back to `context.json` on disk.
   *   Resolve the next handler via `next_handler` frontmatter.
4. **Finalisation**: When `next_handler` is null, the agent outputs the finished payload and terminates. If any errors occur, the **Fallback Handler** compiles and outputs a diagnostic log.

---

## 🧪 Running Evaluations

To verify that the agent conforms to this execution protocol, run the self-scoring evaluation command from your workspace:

```bash
/eval Antigravity/chain-of-responsibility
```
This runs synthetic fixtures (linear pipelines, short-circuits, and loop exceptions) and scores them against the shared rubric.
