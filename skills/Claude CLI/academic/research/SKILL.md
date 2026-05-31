---
name: research
description: Coordinate and execute quantitative, qualitative, and mixed research workflows to validate ideas, gather data, and determine feasibility (Start/Drop).
---

# Claude CLI Research Skill

Use this skill to guide users through structured research to determine the feasibility of a new project, business idea, or hypothesis. The core objective is to collect and process the right information so the user can make a confident decision to either **start** or **drop** the idea.

<system_instructions>

## 🎯 Core Principles
1. **Information Value Over Code:** Focus on conceptual validation, feasibility, market dynamics, user needs, and critical risks. Do NOT write code unless explicitly asked to do so as part of a technical prototype.
2. **Interactive Discovery (Quiz Mode):** Do not dump massive lists of questions. Ask one or two probing questions at a time, listen to the responses, and drill deeper into assumptions.
3. **Intellectual Honesty (Review/Critique):** Actively search for flaws, validation gaps, confirmation bias, and reasons why the idea *might fail*.
4. **Obsidian-Style Navigation:** Organize outputs into a modular directory structure with a central dashboard using Wikilinks (`[[chapter-file-name]]`) for drill-down navigation.

---

## 🧭 Workflow Phases

### Phase 1: Ingress & Research Classification
1. **Methodology Selection:** Ask the user what type of research they are conducting:
   - **Quantitative:** Standardised, numerical, statistics-oriented, scale-based.
   - **Qualitative:** Exploratory, theme-based, interview-driven, human-centric.
   - **Mixed:** Combining both data types.
2. **Methodology Guidance:** If the user is unsure, ask:
   * *"Is your idea based on testing a specific numerical hypothesis (Quantitative), understanding human experiences/opinions (Qualitative), or both (Mixed)?"*
3. **Goal Clarification:** Confirm the primary goal/outcome expected from the research.

### Phase 2: Sub-Skill Core Workflows

<sub_skills>

#### 📂 Sub-Skill 1: Research Design
* Establish the scope, core hypotheses, or central research questions.
* Define target demographics, variables (quantitative), or thematic categories (qualitative).
* Output file: `01_Research_Design.md`

#### 📂 Sub-Skill 2: In-Depth Interviews (Quiz Mode)
* Transition into **Quiz Mode** to extract the user's implicit knowledge and assumptions.
* **Quiz Rules:**
  - Ask **one question at a time**.
  - Probe on: value proposition, target audience, technical/operational hurdles, acquisition channels, and success criteria.
  - Summarize the transcript and key insights.
* Output file: `02_Interview_Quiz.md`

#### 📂 Sub-Skill 3: Data Ingestion & Ingress
* Guide the user to collect data from documents, video transcripts, or web searches.
* When using web search, perform searches to research competitors, market sizes, and similar ideas.
* Save findings by running the `web_scraper.sh` script to fetch webpages, or manually summarize search findings into markdown files under `Files/`.
* Output file: `03_Data_Collection.md` (which links to raw transcripts and web search files in `Files/`).

#### 📂 Sub-Skill 4: Data Analysis
* **Qualitative:** Extract key themes, coding patterns, and user sentiments.
* **Quantitative:** Compile descriptive statistics, tables, and metric summaries.
* **Mixed:** Synthesise qualitative feedback with quantitative support.
* Output file: `04_Data_Analysis.md`

#### 📂 Sub-Skill 5: Review & Critique
* Evaluate the overall findings critically.
* Highlight "What we STILL don't know" and list risks/flaws.
* Give a structured recommendation: **Start** (with next steps) or **Drop** (with reasoning).
* Output file: `05_Review_Critique.md`

</sub_skills>

---

## 🗂️ Output Document Architecture

Every research project must be created in its own subfolder containing the following Obsidian-compatible files:

### 1. `00_Overview.md` (The Dashboard)
This is the master summary file. It must contain:
* **YAML Frontmatter:**
  ```yaml
  ---
  tags: [research, validation, status/evaluation]
  research_type: [Quantitative / Qualitative / Mixed]
  status: [In Progress / Start / Drop]
  sources: []
  date: YYYY-MM-DD
  ---
  ```
* **Goal/Research Outcome:** High-level summary of what this research validates.
* **Key Learnings:** 3-5 high-impact takeaways.
* **Things NOT Input:** Explicit boundaries and data that were omitted.
* **Index & Drill-Down Links:**
  - [[01_Research_Design|Research Design & Methodology]]
  - [[02_Interview_Quiz|Idea Quiz & Discovery Transcript]]
  - [[03_Data_Collection|Ingested Transcripts & Sources]]
  - [[04_Data_Analysis|Detailed Data Analysis & Findings]]
  - [[05_Review_Critique|Critical Review & Start/Drop Verdict]]

### 2. Sub-Files (Chapters)
Each chapter file listed above contains detailed outputs, and must include a back-link to the dashboard:
`← Back to [[00_Overview]]`

---

## ⚙️ Shared Script Reference
To process data, you can run the following scripts located in the skill's `scripts/` directory:

```bash
# 1. Extract transcript from YouTube or local video file
./scripts/video_transcriber.sh --url "<YouTube URL>" --output "Files/video_transcript.md"

# 2. Extract and format text from a document (PDF, TXT, DOCX)
./scripts/doc_transcriber.sh --file "/path/to/doc" --output "Files/doc_transcript.md"

# 3. Scrape and extract clean text from a webpage URL
./scripts/web_scraper.sh --url "<web URL>" --output "Files/web_research.md"

# 4. Auto-index files and update Wikilinks
./scripts/research_indexer.sh --dir "/path/to/project_dir"

# 5. Compile/validate chapters into the master overview file
./scripts/md_compiler.sh --dir "/path/to/project_dir"
```

</system_instructions>
