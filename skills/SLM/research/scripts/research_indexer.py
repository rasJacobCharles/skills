#!/usr/bin/env python3
import os
import re
import sys
import argparse

def parse_frontmatter(content):
    """
    Parses YAML frontmatter from markdown content.
    Returns a dictionary of metadata and the content without frontmatter.
    """
    metadata = {}
    lines = content.splitlines()
    if not lines or lines[0].strip() != '---':
        return metadata, content
        
    fm_lines = []
    content_lines = []
    in_fm = False
    
    for i, line in enumerate(lines):
        if i == 0:
            in_fm = True
            continue
        if in_fm:
            if line.strip() == '---':
                in_fm = False
                content_lines = lines[i+1:]
                break
            fm_lines.append(line)
        else:
            content_lines.append(line)
            
    # Simple parser for basic YAML fields
    for line in fm_lines:
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            # Clean list format like [tag1, tag2] or simple values
            if val.startswith('[') and val.endswith(']'):
                val = [item.strip() for item in val[1:-1].split(',') if item.strip()]
            elif val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            metadata[key] = val
            
    return metadata, "\n".join(content_lines)

def ensure_backlink(file_path):
    """
    Ensures the file has a backlink to the 00_Overview.md file.
    """
    filename = os.path.basename(file_path)
    if filename == '00_Overview.md':
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if backlink already exists
    backlink_pattern = r'\[\[00_Overview\]\]'
    if re.search(backlink_pattern, content):
        return
        
    # Extract frontmatter if it exists
    has_frontmatter = content.startswith('---\n') or content.startswith('---\r\n')
    
    if has_frontmatter:
        # Split frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # Add backlink at the top of the body
            new_body = "\n\n← Back to [[00_Overview]]\n\n" + body.lstrip()
            new_content = f"---{frontmatter}---{new_body}"
        else:
            new_content = "\n\n← Back to [[00_Overview]]\n\n" + content
    else:
        new_content = "\n\n← Back to [[00_Overview]]\n\n" + content
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Added backlink to {filename}")

def index_directory(directory):
    """
    Scans the directory for research files, extracts metadata and builds index metadata.
    """
    files_data = []
    
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith('.md') or filename == '00_Overview.md':
            continue
            
        file_path = os.path.join(directory, filename)
        
        # Ensure the backlink is present
        ensure_backlink(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        metadata, body = parse_frontmatter(content)
        
        # Find first header as title
        title = filename.replace('.md', '').replace('_', ' ')
        for line in body.splitlines():
            if line.startswith('# '):
                title = line[2:].strip()
                break
                
        # Get snippet
        snippet = ""
        for line in body.splitlines():
            clean_line = line.strip()
            if clean_line and not clean_line.startswith('#') and not clean_line.startswith('←'):
                snippet = clean_line[:120] + "..." if len(clean_line) > 120 else clean_line
                break
                
        files_data.append({
            'filename': filename,
            'title': title,
            'tags': metadata.get('tags', []),
            'sources': metadata.get('sources', []),
            'snippet': snippet
        })
        
    return files_data

def update_overview(directory, files_data):
    """
    Updates the 00_Overview.md index section with the scanned files data.
    """
    overview_path = os.path.join(directory, '00_Overview.md')
    if not os.path.exists(overview_path):
        print(f"Warning: 00_Overview.md not found in {directory}. Skipping overview update.")
        return
        
    with open(overview_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Locate frontmatter and extract it
    metadata, body = parse_frontmatter(content)
    
    # Generate new Index and Tag section
    index_lines = ["## 📑 Document Index & Navigation\n"]
    for file in files_data:
        name_no_ext = file['filename'].replace('.md', '')
        tag_str = " ".join([f"`#{t}`" for t in file['tags']])
        index_lines.append(f"* **[[{name_no_ext}|{file['title']}]]** {tag_str}")
        if file['snippet']:
            index_lines.append(f"  > {file['snippet']}\n")
            
    index_markdown = "\n".join(index_lines)
    
    # Replace the existing Index section or append it
    index_header_pattern = r'(## 📑 Document Index & Navigation\n.*?(?=\n##|$))'
    
    # Locate or create the section
    if "## 📑 Document Index & Navigation" in content:
        # Replace existing section
        new_content = re.sub(
            r'## 📑 Document Index & Navigation.*?(?=\n## |$)', 
            index_markdown, 
            content, 
            flags=re.DOTALL
        )
    else:
        # Append to the end of the overview file
        new_content = content.rstrip() + "\n\n" + index_markdown
        
    with open(overview_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated 00_Overview.md with the latest index and Wikilinks.")

def main():
    parser = argparse.ArgumentParser(description="Index files in a research project directory.")
    parser.add_argument("--dir", required=True, help="Path to the research project directory")
    args = parser.parse_args()
    
    if not os.path.isdir(args.dir):
        print(f"Error: Directory not found: {args.dir}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Indexing research directory: {args.dir}...")
    files_data = index_directory(args.dir)
    update_overview(args.dir, files_data)
    print("Indexing complete.")

if __name__ == "__main__":
    main()
