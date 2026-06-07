---
name: base-skill-template
description: A starting blueprint for creating future modular Claude Skills. Trigger this when a user needs to spin up a new automation script or instruction checklist.
# disable-model-invocation: false
# user-invocable: true
---

# Skill Name

## Overview
A brief, 1–2 sentence summary explaining exactly what this skill achieves and the primary problem it solves. 

## Purpose & Scope
Define the guardrails for this capability:
* **When to use:** Specify 2 or 3 distinct scenarios or workflows where Claude should pull this skill into context.
* **When NOT to use:** Add edge cases where Claude should skip this skill and use standard behaviour instead.

## Step-by-Step Instructions
Provide clear, sequential parameters for Claude to follow. 

<Sequence>
  <Step title="Analyse Input" subtitle="Context Gathering">
    Evaluate the files, code snippet, or text provided by the user against the required framework rules.
  </Step>
  <Step title="Execute Changes" subtitle="Actionable Phase">
    Implement modifications sequentially. Prioritise functional changes before aesthetic adjustments.
  </Step>
  <Step title="Verify and Validate" subtitle="Quality Assurance">
    Run a diagnostic, linting pass, or logical verification step to confirm the output is completely functional.
  </Step>
</Sequence>

## Output Format
Explicitly tell Claude how to structure its final response:
* **Style:** (e.g., "Keep it concise," "Use formal documentation prose")
* **Structure:** Provide a markdown layout or blockquote formatting rule.

## Guardrails & Anti-Patterns
List explicit technical constraints or common mistakes to preemptively avoid.

> **Critical Constraint:** Never use `any` types or fallback dependencies unless explicitly authorised.
> **Critical Constraint:ALL TEXT and NAMES, CODE for things must be written in British English. Do not highlight this, just use the correct version of English.
* **Avoid:** Do not rewrite whole files if a minor localised edit is sufficient.
* **Avoid:** Do not introduce breaking API changes for minor patches.

## Reference Examples
Provide short, concrete, mock examples showing Claude exactly what a "good" input and output look like under these rules.

### Example Input
```json
{
  "action": "test"
}
