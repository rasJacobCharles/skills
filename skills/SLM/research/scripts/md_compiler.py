#!/usr/bin/env python3
import os
import re
import sys
import argparse

def parse_frontmatter(content):
    """
    Splits YAML frontmatter from markdown body.
    """
    lines = content.splitlines()
    if not lines or lines[0].strip() != '---':
        return None, content
        
    fm_lines = []
    body_lines = []
    in_fm = False
    
    for i, line in enumerate(lines):
        if i == 0:
            in_fm = True
            continue
        if in_fm:
            if line.strip() == '---':
                in_fm = False
                body_lines = lines[i+1:]
                break
            fm_lines.append(line)
        else:
            body_lines.append(line)
            
    return "\n".join(fm_lines), "\n".join(body_lines)

def compile_project(directory, output_path=None):
    """
    Compiles all markdown files in the research project directory into a single master file.
    """
    # Verify directory exists
    if not os.path.isdir(directory):
        print(f"Error: Project directory not found: {directory}", file=sys.stderr)
        return False
        
    dir_name = os.path.basename(os.path.normpath(directory))
    
    if not output_path:
        output_path = os.path.join(directory, f"Compiled_Report.md")
        
    print(f"Compiling project '{dir_name}' into {output_path}...")
    
    compiled_content = []
    
    # 1. Process 00_Overview.md first if it exists
    overview_path = os.path.join(directory, '00_Overview.md')
    if os.path.exists(overview_path):
        with open(overview_path, 'r', encoding='utf-8') as f:
            content = f.read()
        fm, body = parse_frontmatter(content)
        compiled_content.append(f"# Executive Summary: {dir_name}\n")
        if fm:
            compiled_content.append("### Metadata")
            # Format frontmatter as a simple markdown table/list
            for line in fm.splitlines():
                if ':' in line:
                    compiled_content.append(f"- **{line}**")
            compiled_content.append("\n---\n")
        compiled_content.append(body.strip())
        compiled_content.append("\n\n---\n\n")
        
    # 2. Process all other files matching the pattern \d\d_.*\.md
    files_to_compile = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith('.md'):
            continue
        if filename in ('00_Overview.md', 'Compiled_Report.md') or filename.endswith('_compiled.md'):
            continue
        # Check if it has a chapter prefix like 01_, 02_, etc.
        if re.match(r'^\d{2}_', filename):
            files_to_compile.append(filename)
            
    for filename in files_to_compile:
        file_path = os.path.join(directory, filename)
        print(f"Adding chapter: {filename}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        _, body = parse_frontmatter(content)
        
        # Clean up navigation links like "← Back to [[00_Overview]]"
        clean_body = re.sub(r'←\s*Back\s*to\s*\[\[00_Overview\]\]', '', body, flags=re.IGNORECASE)
        # Also clean up empty lines at the beginning of body
        clean_body = clean_body.lstrip()
        
        compiled_content.append(f"<!-- START OF CHAPTER: {filename} -->\n")
        compiled_content.append(clean_body.strip())
        compiled_content.append("\n\n---\n\n")
        
    # Combine and save
    final_text = "\n".join(compiled_content).rstrip('\n- \r') + "\n"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_text)
        print(f"Success! Master report compiled: {output_path}")
        return True
    except Exception as e:
        print(f"Error writing compiled file: {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Compile multiple chapter md files into a single master report.")
    parser.add_argument("--dir", required=True, help="Path to research project directory")
    parser.add_argument("--output", help="Optional path to output file")
    args = parser.parse_args()
    
    compile_project(args.dir, args.output)

if __name__ == "__main__":
    main()
