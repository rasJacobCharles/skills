---
name: vault-ingester
description: Ingest research papers, blog posts, or YouTube videos, extract key insights, and format them into the family knowledge vault structure.
---

# Custom Harness Vault Ingester Skill

This skill is designed for custom LLM orchestration frameworks and harnesses. It guides the LLM to ingest knowledge from various sources (research papers, blog posts, YouTube videos) and format it into structured, high-quality Obsidian-style markdown notes for the family knowledge vault.

---

## 🎯 Core Principles

1. **Information Density:** Summaries must be technically rich, avoiding high-level hand-waving. Include concrete architectures, algorithms, equations, metrics, and code/configuration where available.
2. **Obsidian Integration:** Every file must contain frontmatter tags, source references, a research type, and a `parent` link using the `[[ParentPage]]` syntax.
3. **Structured Hierarchy:** Always use the exact 5-section layout shown in the template.
4. **Actionable Setup:** Always provide a setup block or usage snippet in the implementation section, helping the user get started immediately.

---

## 🧭 Workflow Phases

### Phase 1: Retrieve Content
* Use the helper script `./scripts/ingest` inside this skill to fetch and clean the source content. Run the command: `./scripts/ingest "<source_url_or_filepath>"`. If the script fails, fallback to `read_url_content` or ask the user to provide a transcript/text copy of the source.

### Phase 2: Identify Parent Page
* Identify where this new note fits in the existing vault. Scan the workspace files (e.g. `family-index.md`, `programming.md`) to find the logical parent page (e.g. `[[programming]]` or `[[artificial-intelligence]]`). Prompt the user if unsure.

### Phase 3: Generate Note
* Generate the note using the exact formatting template. Save the file inside the vault directory with a capitalised name.

### Phase 4: Link Back from Parent
* Edit the parent page (e.g. `programming.md`) to add the new page to its list of child links, preserving the existing format: `[[New Page Name]]`.

---

## 🗂️ Output Document Architecture

### Vault Markdown Template
Use the following template for all ingested vault files:

```markdown
---
tags:
  - <tag-name-1>
  - <tag-name-2>
research_type: <Qualitative | Quantitative | Mixed | Synthesis | Tutorial>
sources:
  - <source-url-or-reference>
parent: "[[<Parent Page Name>]]"
---
**System Overview:**
<Provide a 1-2 paragraph technical summary/overview of the system, paradigm, or project in bold text.>

## 1. Core Problem Statement & Paradigm Shift

### <Existing System Limitations / Traditional Approach>
<Explain the limitations of traditional or baseline approaches, explaining why a change is needed.>

### <The New Paradigm / Proposed Solution>
<Explain the proposed solution, its key innovations, and why it is a paradigm shift.>

---

## 2. Key Architectural Components

### <Component A Name>
*   **Technical Specification:** <Dimensionality, mathematical representation, structural layers, or specific configurations.>
*   **Parameters:** <Model sizes, parameters, types, or attributes.>
*   **Function:** <Detailed operational function and role in the system.>

### <Component B Name>
*   ...

---

## 3. Supported Execution Modes & Topologies

### <Topology/Mode A Name>
*   **Connectivity:** <How data, models, or nodes are connected or structured.>
*   **Interaction Dynamics:** <Step-by-step collaboration loop, message passing, or protocol description.>

### <Topology/Mode B Name>
*   ...

---

## 4. Quantitative Results & Performance Metrics

| <Metric/Baseline Column 1> | <Column 2> | <Column 3> |
| :--- | :--- | :--- |
| <Row 1> | ... | ... |

*<Paragraph explaining the context of the benchmarks, datasets used, and overall performance gains.>*

---

## 5. Implementation & Dependencies

<Provide a clean step-by-step script or code snippet showing how to set up, install, or run the project. Use conda/pip steps where relevant.>

```bash
# Create environment
conda create -n <env_name> python=3.10 -y
conda activate <env_name>

# Install dependencies
pip install -r requirements.txt
```
---
```
