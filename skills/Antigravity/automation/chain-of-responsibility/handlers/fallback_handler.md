---
name: fallback-handler
description: Default handler instructions when a request is unhandled or reaches the terminus without results.
---

# Default Fallback Handler

The Fallback Handler is a safety net placed at the end of the chain or triggered when an intermediate handler encounters an unresolvable error state.

---

## 🎯 Fallback Protocol

When the pipeline routes to this handler:

1. **Verify State**:
   *   Read `context.json`.
   *   Check if `payload['current_output']` is empty, or if `errors[]` contains items.
2. **Action**:
   *   If `errors[]` has items, compile and print a detailed diagnostic report listing all issues from the log history.
   *   If `payload['current_output']` is empty and no errors were logged, append: `"[FallbackException] The request traversed the entire pipeline but was not processed by any handler. Please verify that the input matches the handler requirements."` to `errors[]`.
3. **Save and Report**:
   *   Save the final state back to `context.json`.
   *   Present the final context to the user, highlighting the diagnostic logs.
