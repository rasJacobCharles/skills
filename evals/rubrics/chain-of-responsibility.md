# Chain of Responsibility (CoR) Workflow Rubric

Score each criterion **PASS (1)** / **FAIL (0)** / **N/A**.
N/A criteria are excluded from the denominator.
Final score = sum(PASS) / sum(applicable) × 100.

---

## 1. State & Telemetry Inception (C1)
*   **1.1** Initializes a mutable JSON structure representing the `SharedContext` before running checks. (verify via output logs)
*   **1.2** Tracks total execution step count in `SharedContext['telemetry']['current_step']`. (verify via output logs)
*   **1.3** Tracks individual handler run counts inside `SharedContext['telemetry']['execution_count']`. (verify via output logs)

## 2. Linear Traversal & Chain Forwarding (C2)
*   **2.1** Traverses handlers in the sequence configured in the pipeline configuration. (verify via history log)
*   **2.2** Resolves successor handler via the `next_handler` property of the current active handler. (verify via log)
*   **2.3** Correctly passes the mutated context payload to the next link. (verify via log)

## 3. Short-Circuiting & Guardrails (C3)
*   **3.1** Correctly stops chain processing if any handler fails checks and populates `errors[]`. (verify via log/output)
*   **3.2** Increments handler telemetry count and halts execution with a `LoopException` if execution count reaches 3. (verify via log/output)
*   **3.3** Activates the `Default Fallback Handler` if the pipeline ends without results or logs unhandled errors. (verify via log/output)

## 4. Progressive Disclosure & Filesystem Model (C4)
*   **4.1** Reads and writes `context.json` specifically inside the `[workspace-root]/.cor/runs/<run_id>/` directory to persist state between runs. (verify via read/write log)
*   **4.2** Reads pipeline configurations and handler instruction files dynamically on-demand from the `[workspace-root]/.cor/pipelines/<pipeline_name>/` directory. (verify via logs)
