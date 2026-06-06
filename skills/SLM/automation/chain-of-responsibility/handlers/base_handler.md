---
name: base-handler-template
description: Standard instructions and structure for designing a CoR handler.
next_handler: null
---

# Base Handler Instruction Template

Every handler in a Chain of Responsibility (CoR) pipeline must inherit or conform to this layout. Use this template to create new concrete handlers in your skill folder.

---

## 🗂️ Frontmatter Configuration

Every handler file MUST specify its identity and successor link:
```yaml
---
name: name-of-this-handler
description: Short explanation of what this handler does.
next_handler: name-of-next-handler
---
```

---

## 🎯 Implementation Rules

When executing this specific handler, follow these instructions:

1. **Read State File**: Locate and open the `context.json` file inside the workspace/task folder.
2. **Telemetry Verification**:
   *   Read the handler's execution count: `SharedContext['telemetry']['execution_count'][handler_name]`.
   *   Ensure the count does not violate loops (refer to the [Loop Detector Guardrails](loop_detector.md)).
3. **Execute Core Logic**:
   *   Inspect `payload['current_output']` and `request['input_data']`.
   *   Perform your designated checks, validations, or transformations.
   *   If checks pass, mutate/update `payload['current_output']`.
   *   If validations fail and you must short-circuit, append the error to `errors[]`.
4. **Update State Memory**:
   *   Increment the execution counter: `SharedContext['telemetry']['execution_count'][handler_name] += 1`.
   *   Increment the total steps: `SharedContext['telemetry']['current_step'] += 1`.
   *   Append an entry to `log[]` explaining the modification.
   *   Save the updated JSON context back to `context.json`.
5. **Delegation**:
   *   Read the `next_handler` property.
   *   Invoke the successor handler if specified; otherwise, output the final code and stop.
