---
name: technical-archaeology
description: Scan an existing codebase, detect architectural gaps, and quiz the developer to generate a comprehensive Technical Design Document (TDD).
---

# Claude CLI Technical Archaeology Skill

Use this skill to analyse an existing codebase, map its directory and file structure, identify architectural gaps, and lead an interactive discovery process with the user. The final goal is to generate a comprehensive, professional **Technical Design Document (TDD)** saved directly in the directory where the command is run.

<system_instructions>

## 🎯 Core Principles

1. **Automated Discovery First:** Before asking questions, scan the codebase using `tdd-dig.sh` to extract the directory tree, detect programming languages, and read configuration/package files and any existing `README.md`.
2. **Interactive Gap Resolution (Quiz Mode):** Do not overwhelm the user with long forms. Review the scanner's output, determine the missing components (e.g., undocumented major components, missing design decisions, untracked requirements), and ask **one question at a time** to compile details.
3. **Structured System Design Mapping:** Document the system using industry standard design paradigms (Introduction, High-Level Architecture with Mermaid diagrams, Data/Storage Design, Component breakdowns, and Trade-offs).
4. **Local Portability:** Ensure the resulting document is saved locally as a clean, standardized Markdown file (typically `TECHNICAL_DESIGN.md`).

---

## 🧭 Workflow Phases

<sub_skills>

### Phase 1: Codebase Scanning & Discovery
1. Run `./scripts/tdd-dig.sh --non-interactive --dir <path_to_codebase>` to generate an automated structural map of the project.
2. Read the script's stdout to verify:
   - File tree and detected language distribution.
   - Project dependencies and configurations.
   - Preliminary metadata (name, description) extracted from any existing `README.md`.

### Phase 2: Gap Detection & Quiz Setup
1. Identify components that need functional descriptions (e.g. what does this specific folder or class do?).
2. Note missing architectural flows (how does data flow from user actions to databases/configurations?).
3. Plan target questions for:
   - Problem Statement & Goals.
   - Non-Goals (what is explicitly out of scope).
   - Core design decisions and trade-offs (why this specific tech stack / database).
   - Known limitations, scaling bottlenecks, or technical debt.

### Phase 3: Interactive Dialogue (Quiz Mode)
1. Initiate the quiz. If running programmatically or via terminal, the user can use the script's interactive mode. If running as an agent, the agent should ask the user **one question at a time** in the chat, updating its understanding after each response.
2. Probe on assumptions: if the user mentions using a library or system, ask *why* that choice was made and what alternatives were rejected.

### Phase 4: Formatting & Output Compilation
1. Synthesize all gathered responses with the scanned directory tree.
2. Formulate a clean Markdown document following the TDD Architecture structure.
3. Include an auto-generated or custom **Mermaid** sequence or flow diagram representing the system design.
4. Save the document to `TECHNICAL_DESIGN.md` in the current working directory.

</sub_skills>

---

## 🗂️ Technical Design Document (TDD) Template Architecture

Every generated `TECHNICAL_DESIGN.md` must conform to the following outline:

*   **Header / Metadata:** Title, Authors, Status (Draft/Approved), Date.
*   **1. Introduction & Executive Summary:**
    *   **1.1 Problem Statement:** Concise explanation of the problem solved.
    *   **1.2 System Context:** Core languages, build files, and configuration files.
    *   **1.3 Scope & Requirements:** Bulleted list of In-Scope (Goals) and Out-of-Scope (Non-Goals).
*   **2. System Architecture & High-Level Design:**
    *   **2.1 Codebase structure:** Clean text directory tree.
    *   **2.2 Architecture Description:** Description of how major modules interact.
    *   **2.3 System Diagram:** Mermaid diagram outlining data flow.
*   **3. Data & Storage Design:** Detailed explanation of databases, cache layers, files, or schema models.
*   **4. Detailed Component Design:** Deep-dive sections mapping each major directory/file to its architectural responsibility.
*   **5. Design Decisions & Trade-Offs:** The rationales behind tech choices and alternatives considered.
*   **6. Risks, Assumptions & Future Work:**
    *   **6.1 Known Risks & Limitations:** Technical debt, scaling limits, security assumptions.
    *   **6.2 Future Work:** Roadmap items or planned adjustments.

---

## ⚙️ Script Reference

Use the script inside the skill's `scripts/` directory to scan codebases and automate the quiz process:

```bash
# 1. Start the interactive command line questionnaire (default)
./scripts/tdd-dig.sh --dir "/path/to/project_dir" --output "TECHNICAL_DESIGN.md"

# 2. Run in non-interactive mode to parse the codebase and print structure/gaps in JSON
./scripts/tdd-dig.sh --non-interactive --dir "/path/to/project_dir"
```

</system_instructions>
