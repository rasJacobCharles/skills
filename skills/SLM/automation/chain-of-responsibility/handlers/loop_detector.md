---
name: loop-detector
description: Guardrail rules to detect circular routing and prevent infinite agent execution loops.
---

# Loop Detector Guardrails

To prevent agentic execution loops (e.g. when Handler A fails validation, routes to Handler B, which routes back to Handler A), you must enforce the following check inside every handler:

---

## 🎯 Verification Algorithm

1. Before starting execution, query the current handler's execution count from the state file (`context.json`):
   ```json
   "telemetry": {
     "execution_count": {
       "my-handler-name": 2
     }
   }
   ```
2. **Evaluate Run Counts**:
   *   If the current run count is **less than 3**, increment it and proceed.
   *   If the current run count is **3 or greater**, you must immediately halt the pipeline execution.
3. **Emergency Short-Circuit Action**:
   *   Append a `LoopException` message to `errors[]` (e.g. `"[LoopException] Handler 'my-handler-name' has reached the maximum safety threshold of 3 execution attempts. Aborting."`).
   *   Log the error in the history array.
   *   Save the `context.json` file on disk.
   *   Raise a terminal status failure or report the error directly to the user.
