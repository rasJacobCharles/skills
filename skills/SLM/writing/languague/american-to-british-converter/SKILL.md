---
name: american-to-british-converter
description: Structured spelling and vocabulary conversion from US to UK English optimized for SLMs.
---

# SLM American to British Converter Skill (Optimized)

Use this skill when running under a Small Language Model (SLM) to convert American English to British English.

---

## 🚨 SYSTEM CONSTRAINTS (CRITICAL)
1. **DO NOT WRITE CONVERSION LOGIC BY HAND:** Always invoke `./scripts/converter.sh` for spelling, or `./scripts/measurement_converter.sh` for measurements.
2. **VERIFY DIRECTORY MODIFICATIONS:** Use `--dir` to convert projects in-place.
3. **FILE TYPES LIMIT:** Supports `.txt`, `.md`, `.html`, `.css`, `.js`, `.py`, `.json`, etc.

---

## ⚙️ SCRIPT UTILITIES

Run these bash scripts to convert text:

### Spelling & Vocabulary
```bash
# Convert text string directly
./scripts/converter.sh --text "<text>"

# Convert file in-place
./scripts/converter.sh --file "<file>" --inplace

# Convert directory of text files in-place
./scripts/converter.sh --dir "<directory>"
```

### Measurement Conversion
```bash
# Convert measurements in text
./scripts/measurement_converter.sh --text "<text>"

# Convert measurements in file in-place
./scripts/measurement_converter.sh --file "<file>" --inplace

# Convert measurements in directory in-place
./scripts/measurement_converter.sh --dir "<directory>"
```
