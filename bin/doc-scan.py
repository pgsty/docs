#!/usr/bin/env python3
"""
Scan MDX files in content/docs directory and extract URLs and anchors.

This script:
1. Scans all .mdx files in content/docs/
2. Extracts /docs URLs from file paths
3. Extracts H2/H3 anchors from MDX content
4. Removes trailing slashes, deduplicates, sorts, and outputs to url.md
"""

import os
import sys
import re
from pathlib import Path
from typing import Set, List


def get_project_root(script_path: str) -> Path:
    """Get project root directory from script location."""
    script_dir = Path(script_path).parent.absolute()
    # Assume script is in bin/ directory, so project root is parent
    return script_dir.parent


def path_to_url(file_path: Path, docs_dir: Path) -> str:
    """Convert file path to /docs URL."""
    # Get relative path from docs directory
    rel_path = file_path.relative_to(docs_dir)
    
    # Remove .mdx or .cn.mdx extension
    path_str = str(rel_path)
    if path_str.endswith('.cn.mdx'):
        path_str = path_str[:-7]  # Remove .cn.mdx
    elif path_str.endswith('.mdx'):
        path_str = path_str[:-4]  # Remove .mdx
    
    # Convert index files to directory URLs
    if path_str.endswith('/index'):
        path_str = path_str[:-6]  # Remove /index
    elif path_str == 'index':
        path_str = ''  # Root index becomes empty
    
    # Build /docs URL
    url = '/docs'
    if path_str:
        url += '/' + path_str
    
    return url


def extract_anchors(content: str) -> List[str]:
    """Extract H2 and H3 headers from MDX content and convert to anchor links."""
    anchors = []
    
    # Match ## and ### headers (H2 and H3)
    header_pattern = r'^(#{2,3})\s+(.+)$'
    
    for line in content.split('\n'):
        match = re.match(header_pattern, line.strip())
        if match:
            header_text = match.group(2).strip()
            
            # Convert header text to anchor ID (similar to how MDX/markdown processors do it)
            # Remove markdown formatting, convert to lowercase, replace spaces/special chars with hyphens
            anchor_id = re.sub(r'[^\w\s-]', '', header_text)  # Remove special chars except spaces and hyphens
            anchor_id = re.sub(r'\s+', '-', anchor_id.strip())  # Replace spaces with hyphens
            anchor_id = anchor_id.lower()
            anchor_id = re.sub(r'-+', '-', anchor_id)  # Replace multiple hyphens with single
            anchor_id = anchor_id.strip('-')  # Remove leading/trailing hyphens
            
            if anchor_id:
                anchors.append('#' + anchor_id)
    
    return anchors


def scan_docs_directory(docs_dir: Path) -> Set[str]:
    """Scan docs directory and extract all URLs and anchors."""
    urls = set()
    
    # Find all .mdx files
    mdx_files = list(docs_dir.rglob('*.mdx'))
    
    for file_path in mdx_files:
        # Skip non-documentation files (like meta files)
        if file_path.name.startswith('meta.'):
            continue
            
        # Convert file path to base URL
        base_url = path_to_url(file_path, docs_dir)
        urls.add(base_url)
        
        # Read file content and extract anchors
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            anchors = extract_anchors(content)
            
            # Add anchor URLs
            for anchor in anchors:
                anchor_url = base_url + anchor
                urls.add(anchor_url)
                
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
    
    return urls


def clean_and_sort_urls(urls: Set[str]) -> List[str]:
    """Remove trailing slashes, deduplicate, and sort URLs."""
    # Remove trailing slashes (except for root /docs)
    cleaned = set()
    for url in urls:
        if url != '/docs' and url.endswith('/'):
            url = url.rstrip('/')
        cleaned.add(url)
    
    # Sort URLs
    return sorted(cleaned)


def main():
    """Main function."""
    # Get project root directory
    script_path = os.path.abspath(__file__)
    project_root = get_project_root(script_path)
    
    # Allow custom docs directory as argument
    if len(sys.argv) > 1:
        docs_dir = Path(sys.argv[1]).absolute()
    else:
        docs_dir = project_root / 'content' / 'docs'
    
    if not docs_dir.exists():
        print(f"Error: Docs directory not found: {docs_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Scan directory
    urls = scan_docs_directory(docs_dir)
    
    # Clean and sort
    sorted_urls = clean_and_sort_urls(urls)
    
    # Output to url.md in project root
    output_file = project_root / 'url.md'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for url in sorted_urls:
            f.write(url + '\n')
    
    print(f"Scanned {len(sorted_urls)} URLs to {output_file}")


if __name__ == '__main__':
    main()