#!/usr/bin/env python3
"""
Update master overview diagram from individual stack diagrams.

This script reads all individual stack diagrams and generates
a master overview showing relationships between stacks.
"""

import re
import json
from pathlib import Path
from collections import defaultdict

def extract_stack_info(md_content, stack_name):
    """Extract key information from a stack diagram."""
    info = {
        "name": stack_name,
        "resources": [],
        "dependencies": [],
        "outputs": [],
        "stack_references": []
    }
    
    # Extract resources from the content
    resource_pattern = r'- \*\*(.*?)\*\* \((.*?)\)'
    resources = re.findall(resource_pattern, md_content)
    info["resources"] = [{"name": name, "type": type_} for name, type_ in resources]
    
    # Look for stack references in the content
    stack_ref_pattern = r'StackReference|stack.*reference|depends.*on.*stack'
    if re.search(stack_ref_pattern, md_content, re.IGNORECASE):
        # This is a simplified extraction - in practice you'd parse more carefully
        info["has_stack_references"] = True
    
    return info

def generate_master_overview(stack_infos):
    """Generate master overview diagram from stack information."""
    
    overview = """# Production Infrastructure Overview

## Architecture Summary
Complete overview of all production stacks and their relationships.

## Stack Summary
"""
    
    for stack_info in stack_infos:
        overview += f"- **{stack_info['name']}**: {len(stack_info['resources'])} resources\n"
    
    overview += """
## Master Architecture Diagram

```mermaid
graph TB
    %% Define styles
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef gcp fill:#4285F4,stroke:#1a73e8,stroke-width:2px,color:#fff
    classDef azure fill:#0078D4,stroke:#005a9e,stroke-width:2px,color:#fff
    classDef k8s fill:#326CE5,stroke:#1e3a8a,stroke-width:2px,color:#fff
    classDef db fill:#336791,stroke:#1e3a8a,stroke-width:2px,color:#fff
    classDef lb fill:#28A745,stroke:#155724,stroke-width:2px,color:#fff
    classDef storage fill:#FFC107,stroke:#856404,stroke-width:2px,color:#000
    classDef stack fill:#6C757D,stroke:#495057,stroke-width:3px,color:#fff
    
    subgraph "Production Environment"
"""
    
    # Add each stack as a subgraph with key resources
    for stack_info in stack_infos:
        stack_name = stack_info["name"]
        overview += f'        subgraph "{stack_name.title()}"\n'
        
        # Add key resources (limit to top 3-4 to avoid clutter)
        key_resources = stack_info["resources"][:4]
        for i, resource in enumerate(key_resources):
            clean_name = f"{stack_name}_{resource['name'].replace('-', '_')}"
            resource_type = resource["type"].lower()
            
            # Determine style based on resource type
            if "aws:" in resource_type:
                style = "aws"
            elif "gcp:" in resource_type or "google:" in resource_type:
                style = "gcp"
            elif "database" in resource_type or "db" in resource_type:
                style = "db"
            elif "loadbalancer" in resource_type or "lb" in resource_type:
                style = "lb"
            elif "storage" in resource_type or "bucket" in resource_type:
                style = "storage"
            else:
                style = "aws"
            
            overview += f"            {clean_name}[{resource['name']}]:::{style}\n"
        
        overview += "        end\n\n"
    
    overview += "    end\n\n"
    
    # Add placeholder relationships
    overview += "    %% Stack relationships (update based on actual StackReferences)\n"
    if len(stack_infos) > 1:
        for i in range(len(stack_infos) - 1):
            stack1 = stack_infos[i]["name"]
            stack2 = stack_infos[i + 1]["name"]
            overview += f"    %% {stack1} --> {stack2}\n"
    
    overview += "```\n\n"
    
    # Add detailed breakdown
    overview += "## Stack Details\n\n"
    for stack_info in stack_infos:
        overview += f"### {stack_info['name'].title()}\n"
        overview += f"- **Resources**: {len(stack_info['resources'])}\n"
        if stack_info.get("has_stack_references"):
            overview += "- **Has StackReferences**: Yes\n"
        overview += "\n"
    
    overview += """
## Notes
- Update the relationships section above based on actual StackReferences
- Add external service connections as needed
- Consider security boundaries and network isolation
- Document disaster recovery dependencies
"""
    
    return overview

def main():
    """Generate master overview from individual stack diagrams."""
    repo_root = Path(__file__).parent.parent
    stacks_dir = repo_root / "stacks"
    master_dir = repo_root / "master"
    
    if not stacks_dir.exists():
        print("No stacks directory found")
        return
    
    # Read all stack diagrams
    stack_infos = []
    for stack_file in stacks_dir.glob("*.md"):
        if stack_file.name == ".gitkeep":
            continue
            
        stack_name = stack_file.stem
        try:
            with open(stack_file, 'r') as f:
                content = f.read()
            
            stack_info = extract_stack_info(content, stack_name)
            stack_infos.append(stack_info)
            print(f"Processed stack: {stack_name}")
            
        except Exception as e:
            print(f"Error processing {stack_file}: {e}")
    
    if not stack_infos:
        print("No stack diagrams found to process")
        return
    
    # Generate master overview
    master_content = generate_master_overview(stack_infos)
    
    # Write master overview
    master_dir.mkdir(exist_ok=True)
    master_file = master_dir / "overview.md"
    
    with open(master_file, 'w') as f:
        f.write(master_content)
    
    print(f"Generated master overview: {master_file}")

if __name__ == "__main__":
    main()