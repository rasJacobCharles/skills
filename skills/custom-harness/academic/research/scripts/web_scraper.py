#!/usr/bin/env python3
import os
import sys
import argparse
import urllib.request
from bs4 import BeautifulSoup

def clean_html(html_content):
    """
    Parses HTML, removes scripts/styles, and extracts clean markdown-like text.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted tags
    for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
        element.decompose()
        
    # Standard headers extraction
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        level = int(h.name[1])
        h.replace_with(f"\n\n{'#' * level} {h.get_text().strip()}\n\n")
        
    # Standard paragraphs extraction
    for p in soup.find_all('p'):
        p.replace_with(f"\n{p.get_text().strip()}\n")
        
    # Standard list items extraction
    for li in soup.find_all('li'):
        li.replace_with(f"\n* {li.get_text().strip()}")
        
    # Simple links formatting
    for a in soup.find_all('a', href=True):
        a.replace_with(f" [{a.get_text().strip()}]({a['href']}) ")
        
    # Get clean text
    text = soup.get_text()
    
    # Clean up excessive whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
    
    # Reduce consecutive newlines to at most two
    cleaned_text = re_sub_newlines = '\n'.join(
        line for line in cleaned_text.splitlines()
    )
    
    import re
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    return cleaned_text

def scrape_url(url, output_path):
    print(f"Fetching content from URL: {url}...")
    try:
        import ssl
        context = ssl._create_unverified_context()
        
        # Set User-Agent to avoid blocking by websites
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10, context=context) as response:
            html = response.read()
            
        content = clean_html(html)
        
        # Write to output file
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Web Research Transcript\n\n")
            f.write(f"**Source URL:** {url}\n\n")
            f.write(content)
            f.write("\n")
            
        print(f"Web content successfully scraped and written to {output_path}")
        return True
    except Exception as e:
        print(f"Error scraping URL: {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Scrape and extract clean text from a webpage URL.")
    parser.add_argument("--url", required=True, help="Webpage URL to scrape")
    parser.add_argument("--output", required=True, help="Path to save the output markdown file")
    
    args = parser.parse_args()
    
    scrape_url(args.url, args.output)

if __name__ == "__main__":
    main()
