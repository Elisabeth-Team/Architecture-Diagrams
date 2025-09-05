#!/usr/bin/env python3
"""
Validate all Mermaid diagrams in the repository.

This script checks that all .md files containing Mermaid diagrams
have valid syntax and can be rendered.
"""

import re
import sys
from pathlib import Path

def extract_mermaid_blocks(content):
    """Extract all Mermaid code blocks from markdown content."""
    pattern = r'```mermaid\n(.*?)\n```'
    return re.findall(pattern, content, re.DOTALL)

def validate_mermaid_syntax(mermaid_code):
    """Basic validation of Mermaid syntax."""
    errors = []
    
    # Check for common syntax issues
    lines = mermaid_code.strip().split('\n')
    
    # Check for valid graph declaration
    if not any(line.strip().startswith(('graph', 'flowchart', 'sequenceDiagram', 'classDiagram')) for line in lines):
        errors.append("No valid diagram type declaration found")
    
    # Check for balanced brackets
    open_brackets = mermaid_code.count('[')
    close_brackets = mermaid_code.count(']')
    if open_brackets != close_brackets:
        errors.append(f"Unbalanced brackets: {open_brackets} open, {close_brackets} close")
    
    # Check for balanced parentheses
    open_parens = mermaid_code.count('(')
    close_parens = mermaid_code.count(')')
    if open_parens != close_parens:
        errors.append(f"Unbalanced parentheses: {open_parens} open, {close_parens} close")
    
    return errors

def validate_file(file_path):
    """Validate all Mermaid diagrams in a file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return [f"Error reading file: {e}"]
    
    mermaid_blocks = extract_mermaid_blocks(content)
    if not mermaid_blocks:
        return []  # No Mermaid diagrams to validate
    
    all_errors = []
    for i, block in enumerate(mermaid_blocks):
        errors = validate_mermaid_syntax(block)
        if errors:
            all_errors.extend([f"Block {i+1}: {error}" for error in errors])
    
    return all_errors

def main():
    """Validate all diagram files."""
    repo_root = Path(__file__).parent.parent
    
    # Find all markdown files
    md_files = list(repo_root.glob("**/*.md"))
    
    total_errors = 0
    for md_file in md_files:
        if md_file.name == "README.md":
            continue  # Skip README
            
        errors = validate_file(md_file)
        if errors:
            print(f"\n❌ {md_file.relative_to(repo_root)}:")
            for error in errors:
                print(f"   {error}")
            total_errors += len(errors)
        else:
            print(f"✅ {md_file.relative_to(repo_root)}")
    
    if total_errors > 0:
        print(f"\n❌ Found {total_errors} validation errors")
        sys.exit(1)
    else:
        print(f"\n✅ All diagrams validated successfully")

if __name__ == "__main__":
    main()