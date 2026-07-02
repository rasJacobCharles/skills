---
name: vault-ingester
description: Ingest research papers, blog posts, or YouTube videos, extract key insights, and format them into the family knowledge vault structure.
---

# Vault Ingester Skill

## Goal
Ingest knowledge from various sources (research papers, blog posts, YouTube videos), extract key insights, and format them into structured, high-quality Obsidian-style markdown notes for the family knowledge vault.

## When to Use This Skill
* Use this skill when the user requests to ingest a research paper, blog post, or YouTube video transcript.
* Use this skill when generating structured, high-quality Obsidian-style notes for the family knowledge vault.
* Use this skill to ensure consistency, information density, and structured hierarchy across vault notes.

## Constraints & Rules
* **Information Density:** Summaries must be technically rich, avoiding high-level hand-waving. Include concrete architectures, algorithms, equations, metrics, and code/configuration where available.
* **Obsidian Integration:** Every file must contain frontmatter tags, source references, a research type, and a `parent` link using the `[[ParentPage]]` syntax.
* **Structured Hierarchy:** Always use the exact 5-section layout shown in the template.
* **Actionable Setup:** Always provide a setup block or usage snippet in the implementation section, helping the user get started immediately.
* **File Location & Naming:** Save the file inside the workspace root (e.g. `/Users/jacob/Documents/Personal/family-knowledge-vault/`) with a capitalised, clean name based on the topic (e.g., `Recursive Multi-Agent System.md`).
* **Parent Linking:** Edit the parent page (e.g., `programming.md`) to add the new page to its list of child links, preserving the existing format: `[[New Page Name]]`.
* **Language:** ALL TEXT and NAMES, CODE for things must be written in British English. Do not highlight this, just use the correct version of English (e.g. *behaviour*, *optimise*, *prioritise*, *initialise*, *capitalised*, *synthesise*, *analyse*).

## How to Use It
<Sequence>
  <Step title="Retrieve Content" subtitle="Source Ingestion">
    Use the helper script `./scripts/ingest` inside this skill to fetch and clean the source content. Run the command: `./scripts/ingest "<source_url_or_filepath>"`. If the script fails, fallback to `read_url_content` or ask the user to provide a transcript/text copy of the source.
  </Step>
  <Step title="Identify Parent" subtitle="Hierarchy Alignment">
    Identify where this new note fits in the existing vault. Scan the workspace files (e.g., look at `family-index.md`, `programming.md`) to find the logical parent page (e.g. `[[programming]]` or `[[artificial-intelligence]]`). If unsure, ask the user to specify or confirm the parent.
  </Step>
  <Step title="Generate Note" subtitle="Obsidian Formatting">
    Generate the note using the exact formatting template. Save the file inside the vault directory with a capitalised name.
  </Step>
  <Step title="Link Back" subtitle="Parent Linkage">
    Edit the parent page (e.g., `programming.md`) to add the new page to its list of child links, preserving the existing format: `[[New Page Name]]`.
  </Step>
</Sequence>

## Reference Examples

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
