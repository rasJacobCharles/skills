---
name: american-to-british-converter
description: Convert text and files from American English spelling and vocabulary to British English (UK English).
---

# Claude CLI American to British English Converter Skill

Use this skill to convert text, individual files, or entire directories from American English (US) spelling and vocabulary to British English (UK) spelling and vocabulary.

<system_instructions>

## 🎯 Core Principles

1. **Precision Spelling Substitution:** Standard spelling rules (e.g. `-ize` to `-ise`, `-yze` to `-yse`, and doubling ending consonants like `traveler` to `traveller`) are automatically applied using regex, while ignoring exceptions like `size` or `seize`.
2. **Context-Aware Vocabulary Mapping:** Common vocabulary differences (e.g. `apartment` to `flat`, `elevator` to `lift`, and foods like `zucchini` to `courgette`) are mapped using an exact-match case-preserving dictionary.
3. **Measurement System Localisation:** Conversions for US Customary units to Metric/UK equivalents (e.g. `Fahrenheit` to `Celsius`, `pounds` to `kg`, `gallons` to `litres`, `fluid ounces` to `ml`, `inches` to `cm`, `feet`/`yards` to `meters`) are handled systematically via a dedicated helper script.
4. **Preservation of Case:** Substitutions respect the case pattern of the source word (e.g. `Color` -> `Colour`, `COLOR` -> `COLOUR`, `color` -> `colour`).
5. **Safety & Directory Processing:** Only text-based file extensions (like `.txt`, `.md`, `.py`, `.js`, `.json`, `.html`, etc.) are processed during directory conversions to avoid corrupting binaries.

---

## ⚙️ Script Reference

To convert text, you can run the following shell commands located in the skill's `scripts/` directory:

### Spelling & Vocabulary Converter
```bash
# 1. Convert text directly from the CLI
./scripts/converter.sh --text "<American English text>"

# 2. Convert a file in-place
./scripts/converter.sh --file "path/to/input.txt" --inplace

# 3. Convert an entire directory of text files recursively in-place
./scripts/converter.sh --dir "path/to/project_dir"
```

### Measurement Converter
```bash
# 1. Convert text measurements directly from the CLI
./scripts/measurement_converter.sh --text "<Text containing US measurements>"

# 2. Convert a file's measurements in-place
./scripts/measurement_converter.sh --file "path/to/input.txt" --inplace

# 3. Convert measurements across an entire directory recursively in-place
./scripts/measurement_converter.sh --dir "path/to/project_dir"
```

</system_instructions>
