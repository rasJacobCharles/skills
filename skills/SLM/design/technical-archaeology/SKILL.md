---
name: technical-archaeology
description: Scan an existing codebase, detect architectural gaps, and quiz the developer to generate a Technical Design Document (TDD).
---

# SLM Technical Archaeology Skill (Optimized)

Use this skill when running a Small Language Model (SLM) under 10B parameters. Keep context small and follow these instructions strictly.

---

## 🚨 SYSTEM CONSTRAINTS (CRITICAL)
1. **DO NOT WRITE CODE** unless explicitly requested.
2. **ASK ONE QUESTION AT A TIME** in Quiz Mode. Do not output lists of questions.
3. **DO NOT EXCEED CONTEXT LIMITS:** Keep quizzes and transcripts brief.
4. **USE BASH SCRIPTS** in `scripts/` to do codebase structure scans.

---

## 🧭 WORKFLOW

### Phase 1: Scan & Discovery
1. Run `./scripts/tdd-dig.sh --non-interactive --dir <path>` to get project structure and gaps in JSON.
2. Review the languages, configs, and file tree.

### Phase 2: Quiz Mode (Interactive Dialogue)
1. Ask the user one probing question at a time to resolve gaps:
   - What is the primary problem this system solves?
   - What are the main goals and non-goals?
   - What is the responsibility of each main file/folder?
   - What design decisions, tech choices, or trade-offs were made?
   - What are the risks or future work?

### Phase 3: Compilation
1. Generate `TECHNICAL_DESIGN.md` in the current folder using the gathered details.

---

## 🗂️ FILE STRUCTURE
The generated `TECHNICAL_DESIGN.md` must include:
* **Metadata:** Title, Authors, Status, Date.
* **1. Introduction:** Problem statement, Goals, and Non-Goals.
* **2. Architecture:** File tree, High-level flow, and Mermaid diagram.
* **3. Storage:** Database or file layout.
* **4. Components:** 1-2 sentence description of key directories/files.
* **5. Trade-offs:** Technology choice rationales.
* **6. Risks & Roadmap:** Limitations and future work.

---

## ⚙️ SCRIPT UTILITIES

Run these scripts to scan and draft:

```bash
# 1. Start interactive command-line quiz
./scripts/tdd-dig.sh --dir "." --output "TECHNICAL_DESIGN.md"

# 2. Run codebase scanner in non-interactive mode
./scripts/tdd-dig.sh --non-interactive --dir "."
```
