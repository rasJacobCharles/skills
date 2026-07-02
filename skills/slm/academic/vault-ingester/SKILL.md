---
name: vault-ingester
description: Ingest research papers, blog posts, or YouTube videos, extract key insights, and format them into the family knowledge vault structure.
---

# SLM Vault Ingester Skill (Optimized)

Use this skill when running a Small Language Model (SLM) under 10B parameters. Keep context small and follow these instructions strictly.

---

## 🚨 SYSTEM CONSTRAINTS (CRITICAL)

1. **DETERMINISTIC STRUCTURE:** Use the exact 5-section layout and bolded System Overview from the template.
2. **BRITISH ENGLISH:** All text and names must be written in British English.
3. **USE HELPER SCRIPT:** Always call `./scripts/ingest` to extract content.
4. **LINK TO PARENT:** Add the new page link `[[New Page Name]]` to the parent file.
5. **INTERACTIVE PARENT PROMPT:** Ask the user to confirm/specify the parent if not provided.

---

## 🧭 WORKFLOW

### Phase 1: Retrieve Content
* Run the helper script: `./scripts/ingest "<source_url_or_filepath>"` to fetch/clean content.

### Phase 2: Parent Alignment
* Find parent in workspace (e.g. `programming.md`). Ask if missing.

### Phase 3: Generate Note
* Write note using template. Save with capitalised name to vault root.

### Phase 4: Link Back
* Add `[[New Page Name]]` link to parent file.

---

## 🗂️ FILE STRUCTURE

### Vault Markdown Template
```markdown
---
tags:
  - <tag-name-1>
research_type: <Qualitative | Quantitative | Mixed | Synthesis | Tutorial>
sources:
  - <source-url-or-reference>
parent: "[[<Parent Page Name>]]"
---
**System Overview:**
<1-2 paragraph summary in bold text.>

## 1. Core Problem Statement & Paradigm Shift
### <Traditional Limitations>
### <Proposed Solution>

---
## 2. Key Architectural Components
### <Component Name>
* **Technical Specification:**
* **Parameters:**
* **Function:**

---
## 3. Supported Execution Modes & Topologies
### <Topology Name>
* **Connectivity:**
* **Interaction Dynamics:**

---
## 4. Quantitative Results & Performance Metrics
| Metric | Baseline | Proposed |
| :--- | :--- | :--- |

---
## 5. Implementation & Dependencies
```bash
conda create -n <env_name> python=3.10 -y
conda activate <env_name>
pip install -r requirements.txt
```
---
```

---

## ⚙️ SCRIPT UTILITIES
```bash
./scripts/ingest "<source_url_or_filepath>"
```
