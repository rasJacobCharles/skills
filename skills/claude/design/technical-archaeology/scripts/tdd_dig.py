#!/usr/bin/env python3
import os
import sys
import argparse
import re
import json

def get_ignore_list():
    return {
        '.git', 'node_modules', 'venv', '.venv', '__pycache__', 'build', 'dist',
        '.eggs', '*.egg-info', '.DS_Store', '.idea', '.vscode', 'out', 'target',
        '.venv', 'bower_components', 'logs', '*.log', '.gemini', 'artifacts'
    }

def should_ignore(name, ignore_list):
    if name in ignore_list:
        return True
    for pattern in ignore_list:
        if pattern.startswith('*') and name.endswith(pattern[1:]):
            return True
        if pattern.endswith('*') and name.startswith(pattern[:-1]):
            return True
    return False

def generate_file_tree(startpath, max_depth=3):
    ignore_list = get_ignore_list()
    tree_lines = []
    
    def _recurse(dir_path, depth, prefix=""):
        if depth > max_depth:
            return
        try:
            entries = sorted(os.listdir(dir_path))
        except Exception:
            return
            
        entries = [e for e in entries if not should_ignore(e, ignore_list)]
        
        for i, entry in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            full_path = os.path.join(dir_path, entry)
            is_dir = os.path.isdir(full_path)
            
            tree_lines.append(f"{prefix}{connector}{entry}{'/' if is_dir else ''}")
            
            if is_dir:
                next_prefix = prefix + ("    " if is_last else "│   ")
                _recurse(full_path, depth + 1, next_prefix)
                
    root_name = os.path.basename(os.path.abspath(startpath)) or "root"
    tree_lines.append(f"{root_name}/")
    _recurse(startpath, 1)
    return "\n".join(tree_lines)

def detect_languages_and_frameworks(startpath):
    ignore_list = get_ignore_list()
    ext_counts = {}
    found_configs = []
    
    for root, dirs, files in os.walk(startpath):
        # Prune ignored directories in place
        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_list)]
        
        for file in files:
            if should_ignore(file, ignore_list):
                continue
                
            # Count extensions
            _, ext = os.path.splitext(file)
            if ext:
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
                
            # Detect config files
            if file in ['package.json', 'requirements.txt', 'go.mod', 'Cargo.toml', 
                        'setup.py', 'composer.json', 'Gemfile', 'build.gradle', 'pom.xml']:
                found_configs.append(file)
                
    # Map common extensions to languages
    lang_mapping = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.tsx': 'React/TypeScript',
        '.jsx': 'React/JavaScript',
        '.go': 'Go',
        '.rs': 'Rust',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.h': 'C/C++ Header',
        '.cs': 'C#',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.sh': 'Shell Script',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.md': 'Markdown',
        '.html': 'HTML',
        '.css': 'CSS'
    }
    
    languages = {}
    for ext, count in ext_counts.items():
        lang = lang_mapping.get(ext.lower(), f"Other ({ext})")
        languages[lang] = languages.get(lang, 0) + count
        
    # Sort languages by file count descending
    sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    return sorted_languages, found_configs

def parse_readme(startpath):
    readme_path = None
    for file in os.listdir(startpath):
        if file.lower() == 'readme.md':
            readme_path = os.path.join(startpath, file)
            break
            
    if not readme_path or not os.path.exists(readme_path):
        return None, None
        
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Try to find the title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else None
        
        # Try to find the description (text after title, before next header)
        description = None
        if title_match:
            start_pos = title_match.end()
            next_header_match = re.search(r'^##?\s+', content[start_pos:], re.MULTILINE)
            if next_header_match:
                end_pos = start_pos + next_header_match.start()
                desc_text = content[start_pos:end_pos].strip()
            else:
                desc_text = content[start_pos:].strip()
                
            # Clean up desc_text (remove badges, images, etc.)
            desc_lines = []
            for line in desc_text.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith('[!') or line.startswith('<img') or line.startswith('![') or line.startswith('[') and 'http' in line:
                    continue
                desc_lines.append(line)
            description = "\n".join(desc_lines[:3]) if desc_lines else None
            
        return title, description
    except Exception:
        return None, None

def get_key_components(startpath):
    ignore_list = get_ignore_list()
    components = []
    
    # Check top-level directories
    try:
        entries = sorted(os.listdir(startpath))
    except Exception:
        return []
        
    for entry in entries:
        if should_ignore(entry, ignore_list):
            continue
        full_path = os.path.join(startpath, entry)
        if os.path.isdir(full_path):
            components.append({
                'name': entry,
                'type': 'directory',
                'path': entry
            })
        elif os.path.isfile(full_path) and not entry.startswith('.'):
            # Only include major files
            _, ext = os.path.splitext(entry)
            if ext in ['.py', '.js', '.ts', '.go', '.rs', '.java', '.cs', '.sh', '.rb', '.php']:
                components.append({
                    'name': entry,
                    'type': 'file',
                    'path': entry
                })
    return components

def run_interactive_quiz(metadata, key_components):
    print("=" * 60)
    print("         TECHNICAL ARCHAEOLOGY - QUIZ MODE")
    print("=" * 60)
    print("I will ask you a series of questions to generate a detailed")
    print("Technical Design Document (TDD) for your project.")
    print("If you don't know an answer, just press Enter to skip or flag it.")
    print("-" * 60)
    
    responses = {}
    
    # 1. Title and Metadata
    default_title = metadata.get('readme_title') or metadata.get('dir_name')
    print(f"\n[1/7] Document Meta")
    responses['title'] = input(f"Project/System Name [{default_title}]: ").strip() or default_title
    responses['author'] = input("Authors (comma-separated) [Archaeology Agent]: ").strip() or "Archaeology Agent"
    responses['status'] = input("Document Status (e.g. Draft, Approved, Proposed) [Draft]: ").strip() or "Draft"
    
    # 2. Introduction & Problem Statement
    default_desc = metadata.get('readme_desc') or ""
    print(f"\n[2/7] Introduction & Problem Statement")
    print(f"Describe the primary problem this project solves and its core value.")
    if default_desc:
        print(f"Auto-detected from README: \"{default_desc}\"")
        use_default = input("Use this description? (y/n) [y]: ").strip().lower() != 'n'
        if use_default:
            responses['problem_statement'] = default_desc
        else:
            responses['problem_statement'] = input("Describe the problem: ").strip()
    else:
        responses['problem_statement'] = input("Describe the problem: ").strip()
        
    responses['goals'] = input("What are the key goals/in-scope requirements? (use semicolons to separate): ").strip()
    responses['non_goals'] = input("What is explicitly out of scope / non-goals? (use semicolons to separate): ").strip()

    # 3. System Architecture
    print(f"\n[3/7] System Architecture")
    responses['architecture_desc'] = input("Give a high-level explanation of the system architecture & data flow: ").strip()
    
    # 4. Component Responsibilities
    print(f"\n[4/7] Component Responsibilities")
    print("I've identified these key directories/files in the codebase.")
    print("Please explain the responsibility of each:")
    component_docs = {}
    for comp in key_components[:6]: # Limit to first 6 major components to prevent fatigue
        comp_name = comp['name']
        comp_type = comp['type']
        desc = input(f" - {comp_name} ({comp_type}): ").strip()
        if desc:
            component_docs[comp_name] = desc
    responses['component_responsibilities'] = component_docs

    # 5. Data & Storage
    print(f"\n[5/7] Data & Storage Design")
    responses['data_design'] = input("How is data stored, managed, or structured? (databases, schemas, file systems): ").strip()

    # 6. Design Decisions & Trade-Offs
    print(f"\n[6/7] Design Decisions & Trade-Offs")
    responses['decisions'] = input("Why was this technology stack/architecture chosen? What alternatives were rejected?: ").strip()

    # 7. Risks & Future Work
    print(f"\n[7/7] Risks, Assumptions & Future Work")
    responses['risks'] = input("What are the main risks, limitations, or technical debt in this system?: ").strip()
    responses['future_work'] = input("What are the next planned steps or improvements?: ").strip()

    return responses

def format_tdd_markdown(responses, metadata, file_tree):
    # Format lists
    goals_list = ""
    if responses.get('goals'):
        goals_list = "\n".join(f"- {g.strip()}" for g in responses['goals'].split(';') if g.strip())
    else:
        goals_list = "- Define core system capabilities."
        
    non_goals_list = ""
    if responses.get('non_goals'):
        non_goals_list = "\n".join(f"- {ng.strip()}" for ng in responses['non_goals'].split(';') if ng.strip())
    else:
        non_goals_list = "- Future scaling and UI extensions."

    # Language/Config Info
    lang_str = ", ".join(f"{lang} ({count} files)" for lang, count in metadata.get('languages', [])[:3])
    config_str = ", ".join(metadata.get('configs', [])) or "None detected"

    # Component breakdown
    component_lines = []
    comp_docs = responses.get('component_responsibilities', {})
    for comp_name, comp_desc in comp_docs.items():
        component_lines.append(f"### `{comp_name}`\n{comp_desc}\n")
    component_str = "\n".join(component_lines) if component_lines else "*No component descriptions provided.*"

    md = f"""# Technical Design Document: {responses['title']}

**Authors:** {responses['author']}  
**Status:** `{responses['status']}`  
**Date:** {os.popen('date "+%Y-%m-%d"').read().strip()}

---

## 1. Introduction & Executive Summary

### 1.1 Problem Statement
{responses.get('problem_statement') or '*No problem statement provided.*'}

### 1.2 System Context
- **Primary Languages:** {lang_str or 'Unknown'}
- **Build/Config Files:** {config_str}

### 1.3 Scope & Requirements

#### In-Scope (Goals)
{goals_list}

#### Out-of-Scope (Non-Goals)
{non_goals_list}

---

## 2. System Architecture & High-Level Design

### 2.1 Codebase structure
```text
{file_tree}
```

### 2.2 System Architecture Description
{responses.get('architecture_desc') or '*No architecture description provided.*'}

### 2.3 Proposed Data Flow Diagram (Mermaid)
```mermaid
graph TD
    User([User / Client]) --> Controller[Main Controller / Entrypoint]
    Controller --> Services[Core Business Logic]
    Services --> DB[(Data Storage / Configs)]
```

---

## 3. Data & Storage Design
{responses.get('data_design') or '*No data design or storage strategy described.*'}

---

## 4. Detailed Component Design

{component_str}

---

## 5. Design Decisions & Trade-Offs
{responses.get('decisions') or '*No design decisions or trade-offs documented.*'}

---

## 6. Risks, Assumptions & Future Work

### 6.1 Known Risks & Limitations
{responses.get('risks') or '*No specific risks or technical limitations defined.*'}

### 6.2 Future Work
{responses.get('future_work') or '*No future improvements or tasks specified.*'}
"""
    return md

def main():
    parser = argparse.ArgumentParser(description="Technical Archaeology: Dig into a codebase and generate a Technical Design Document.")
    parser.add_argument("--dir", "-d", default=".", help="Codebase directory to scan")
    parser.add_argument("--output", "-o", default="TECHNICAL_DESIGN.md", help="Output Markdown file name")
    parser.add_argument("--non-interactive", action="store_true", help="Scan codebase and output details/gaps in JSON without quizzing")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.dir):
        print(f"Error: Directory '{args.dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    # Run code mapping
    print(f"Scanning codebase: {os.path.abspath(args.dir)}...")
    languages, configs = detect_languages_and_frameworks(args.dir)
    readme_title, readme_desc = parse_readme(args.dir)
    key_components = get_key_components(args.dir)
    file_tree = generate_file_tree(args.dir, max_depth=2)
    
    metadata = {
        'dir_name': os.path.basename(os.path.abspath(args.dir)),
        'readme_title': readme_title,
        'readme_desc': readme_desc,
        'languages': languages,
        'configs': configs,
    }
    
    if args.non_interactive:
        # Output analysis results in JSON format
        output_data = {
            'metadata': metadata,
            'file_tree': file_tree,
            'key_components': key_components,
            'detected_gaps': [
                "Define executive summary & business problem statement",
                "Define architectural/data flows between components",
                f"Describe responsibilities for components: {', '.join(c['name'] for c in key_components[:6])}",
                "Document technical trade-offs & technology choice rationale",
                "Identify external assumptions, scaling limits, and dependencies"
            ]
        }
        print(json.dumps(output_data, indent=2))
        return
        
    # Interactive quiz mode
    responses = run_interactive_quiz(metadata, key_components)
    
    # Generate markdown content
    tdd_md = format_tdd_markdown(responses, metadata, file_tree)
    
    # Save output file
    output_path = args.output
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(tdd_md)
        print(f"\nSuccess! Technical Design Document successfully written to: {os.path.abspath(output_path)}")
    except Exception as e:
        print(f"\nError writing output file: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
