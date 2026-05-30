#!/usr/bin/env python3
import os
import sys
import argparse
import csv

def extract_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def extract_pdf(file_path):
    try:
        import pypdf
    except ImportError:
        return "Error: 'pypdf' python package is missing from the environment."
        
    try:
        reader = pypdf.PdfReader(file_path)
        pages_content = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            pages_content.append(f"## Page {i + 1}\n\n{text}\n")
        return "\n".join(pages_content)
    except Exception as e:
        return f"Error parsing PDF file: {str(e)}"

def extract_docx(file_path):
    try:
        import docx
    except ImportError:
        return "Error: 'python-docx' python package is missing from the environment."
        
    try:
        doc = docx.Document(file_path)
        paragraphs = []
        for p in doc.paragraphs:
            if p.text.strip():
                paragraphs.append(p.text)
        return "\n\n".join(paragraphs)
    except Exception as e:
        return f"Error parsing Word Document: {str(e)}"

def extract_csv(file_path):
    try:
        lines = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if not headers:
                return "Empty CSV file."
                
            # Make markdown header
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            
            for row in reader:
                # pad or slice row to match headers count
                row_cells = row + [""] * (len(headers) - len(row))
                row_cells = row_cells[:len(headers)]
                # escape pipe chars
                row_cells = [cell.replace('|', '\\|') for cell in row_cells]
                lines.append("| " + " | ".join(row_cells) + " |")
                
        return "\n".join(lines)
    except Exception as e:
        return f"Error parsing CSV file: {str(e)}"

def extract_html(file_path):
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        # Fallback to crude regex/replace if BS4 is missing
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        import re
        text = re.sub('<[^<]+?>', '', html)
        return text
        
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text_content = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text_content
    except Exception as e:
        return f"Error parsing HTML: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Extract clean text/markdown from documents.")
    parser.add_argument("--file", required=True, help="Path to document to transcribe")
    parser.add_argument("--output", required=True, help="Path to save the output markdown file")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: Source file does not exist: {args.file}", file=sys.stderr)
        sys.exit(1)
        
    ext = os.path.splitext(args.file.lower())[1]
    
    print(f"Extracting content from: {args.file} ({ext})...")
    
    if ext == '.pdf':
        content = extract_pdf(args.file)
    elif ext in ('.docx', '.doc'):
        content = extract_docx(args.file)
    elif ext == '.csv':
        content = extract_csv(args.file)
    elif ext in ('.html', '.htm'):
        content = extract_html(args.file)
    elif ext in ('.txt', '.md', '.markdown'):
        content = extract_txt(args.file)
    else:
        print(f"Unsupported file extension {ext}. Treating as plain text...", file=sys.stderr)
        content = extract_txt(args.file)
        
    # Write output
    try:
        # Create output dir if needed
        out_dir = os.path.dirname(args.output)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
            
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"# Document Transcript\n\n")
            f.write(f"**Source Document:** {os.path.basename(args.file)}\n\n")
            f.write(content)
            f.write("\n")
        print(f"Document content successfully extracted and written to {args.output}")
    except Exception as e:
        print(f"Error writing output to {args.output}: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
