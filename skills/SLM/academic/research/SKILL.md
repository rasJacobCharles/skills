---
name: research
description: Structured research and validation workflow for Small Language Models (SLMs) to decide whether to Start or Drop an idea.
---

# SLM Research Skill (Optimized)

Use this skill when running a Small Language Model (SLM) under 10B parameters. Keep context small and follow these instructions strictly.

---

## 🚨 SYSTEM CONSTRAINTS (CRITICAL)
1. **DO NOT WRITE CODE** unless explicitly requested.
2. **ASK ONE QUESTION AT A TIME** in Quiz Mode. Do not output lists of questions.
3. **DO NOT EXCEED CONTEXT LIMITS:** Summarize inputs early and keep transcripts short.
4. **USE BASH SCRIPTS** in `scripts/` to do heavy text extraction.

---

## 🧭 WORKFLOW

### Phase 1: Classification
1. Ask the user: *"Are you doing Quantitative, Qualitative, or Mixed research?"*
2. Confirm the main validation goal (feasibility study).

### Phase 2: Execution Steps
1. **Research Design:** Create `01_Research_Design.md` with core hypotheses.
2. **Quiz Mode (In-Depth Interview):** 
   - Ask the user one probing question at a time to challenge assumptions.
   - Summarize answers into `02_Interview_Quiz.md`.
3. **Data Ingestion:** Use `video_transcriber.sh`, `doc_transcriber.sh`, or `web_scraper.sh` to extract text. Save to `Files/` folder. Create `03_Data_Collection.md`.
4. **Analysis:** Identify 3-5 main insights. Create `04_Data_Analysis.md`.
5. **Critique:** Identify risks. Write a "Start" or "Drop" recommendation in `05_Review_Critique.md`.

---

## 🗂️ FILE STRUCTURE
Create these files in a project folder:
* `00_Overview.md` (Dashboard with metadata, goals, key learnings, things NOT input, and Wikilinks to chapters)
* `01_Research_Design.md`
* `02_Interview_Quiz.md`
* `03_Data_Collection.md`
* `04_Data_Analysis.md`
* `05_Review_Critique.md`

All chapter files must end with a link back to the overview:
`← Back to [[00_Overview]]`

---

## ⚙️ SCRIPT UTILITIES
Run these bash scripts to parse data and update files:

```bash
# Get video transcripts
./scripts/video_transcriber.sh --url "<URL>" --output "Files/video_transcript.md"

# Parse documents (PDF/DOCX/TXT/CSV)
./scripts/doc_transcriber.sh --file "<file>" --output "Files/doc_transcript.md"

# Scrape webpages
./scripts/web_scraper.sh --url "<web URL>" --output "Files/web_research.md"

# Update index and Wikilinks in 00_Overview.md
./scripts/research_indexer.sh --dir "."

# Compile report
./scripts/md_compiler.sh --dir "."
```
