---
name: chain-of-responsibility
description: Design, instantiate, and execute task workflows using the Chain of Responsibility (CoR) pattern with agentic systems.
---

# Agentic Chain of Responsibility (CoR) Workflow Skill

Use this skill to decompose complex, multi-stage task execution, content generation, or code validation into a sequence of decoupled, single-responsibility agent instructions (handlers).

---

## 🏛️ Context Engineering & Progressive Disclosure

This skill is designed around **progressive disclosure**. Rather than loading all instructions into your immediate context window, you should read these linked files on-demand as they become relevant during execution:

1. **The State Memory**: The **Shared Context** is stored as a persistent file on disk (`context.json` or `context.md` in the current task folder). This allows different agents and handlers to read and write state memory across runs.
   *   Read the detailed structure here: **[Context JSON Schema](schema/context_schema.json)**

2. **Creating & Running Handlers**:
   *   Learn how to structure a handler skill file: **[Base Handler Template](handlers/base_handler.md)**
   *   How to handle routing loops and recursion limits: **[Loop Detector Guardrails](handlers/loop_detector.md)**
   *   How to handle unconsumed requests: **[Default Fallback Handler](handlers/fallback_handler.md)**

3. **Concrete Implementation Examples**:
   *   Browse pre-configured pipeline files: **[Pipeline Examples Index](examples/README.md)**

---

## 📂 Persistent Storage & Workspace Location

To ensure portability, version-control compatibility, and transparency, all created chains and active execution states are stored locally in the target project workspace:

1. **Pipeline Definitions**: 
   When a new chain is created, its configuration schema and concrete handler files are saved to:
   `[project-root]/.cor/pipelines/<pipeline_name>/`
   *   `pipeline.yaml`: The YAML schema declaring execution order and fallback handlers.
   *   `handlers/`: Folder containing the individual handler instruction markdown files (e.g. `CleanTextHandler.md`).
   
2. **Active Execution Runs**:
   The active Shared Context JSON payload is persisted on disk to:
   `[project-root]/.cor/runs/<run_id>/context.json`
   This is the file that handlers read and update dynamically as the request travels along the chain.

---

## 🧭 Pipeline Execution Protocol

When executing a CoR workflow, you must act as the chain runner and follow this protocol:

1. **Ingress**: Read the input data and the pipeline configuration file (`pipeline.yaml`).
2. **Context Creation**: Write the initial state memory file (`context.json`) following the [Schema](schema/context_schema.json).
3. **Execution Loop**:
   *   Identify the current active handler from the pipeline configuration.
   *   Read the handler's skill markdown file.
   *   Read the `context.json` file.
   *   Execute the handler's checks or transformations.
   *   Update `context.json` (mutating the payload, incrementing telemetry counters, and appending to the log).
   *   Read the `next_handler` property.
   *   If `next_handler` is not null, load the successor and repeat this loop.
   *   If `next_handler` is null, finalize and return the output.
