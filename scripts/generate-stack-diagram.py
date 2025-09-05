#!/usr/bin/env python3
"""
Generate architecture diagram from Pulumi stack export.

Usage:
    python generate-stack-diagram.py <stack-name> [--project <project>] [--org <org>]

This script exports a Pulumi stack and generates a Mermaid diagram
showing the resources and their relationships.
"""

import json
import argparse
import subprocess
import sys
from pathlib import Path

def get_stack_export(stack_name, project=None, org=None):
    """Export stack configuration and resources."""
    cmd = ["pulumi", "stack", "export", "--stack", stack_name]
    if project:
        cmd.extend(["--cwd", project])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error exporting stack {stack_name}: {e.stderr}")
        return None

def get_resource_type_style(resource_type):
    """Map resource types to Mermaid CSS classes."""
    type_lower = resource_type.lower()
    
    if "aws:" in type_lower:
        return "aws"
    elif "gcp:" in type_lower or "google:" in type_lower:
        return "gcp"
    elif "azure:" in type_lower:
        return "azure"
    elif "kubernetes:" in type_lower or "k8s:" in type_lower:
        return "k8s"
    elif any(db in type_lower for db in ["database", "db", "sql", "postgres", "mysql", "mongo"]):
        return "db"
    elif any(lb in type_lower for lb in ["loadbalancer", "alb", "nlb", "elb"]):
        return "lb"
    elif any(storage in type_lower for storage in ["bucket", "storage", "s3", "blob"]):
        return "storage"
    else:
        return "aws"  # default

def generate_mermaid_diagram(stack_export, stack_name):
    """Generate Mermaid diagram from stack export."""
    resources = stack_export.get("deployment", {}).get("resources", [])
    
    diagram = f"""# {stack_name.title()} Architecture

## Overview
Architecture diagram for the {stack_name} stack.

## Architecture Diagram

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
    
    subgraph "Stack: {stack_name}"
"""
    
    # Add resources
    resource_nodes = {}
    for i, resource in enumerate(resources):
        if resource.get("type") == "pulumi:pulumi:Stack":
            continue
            
        urn = resource.get("urn", "")
        resource_type = resource.get("type", "")
        resource_name = urn.split("::")[-1] if "::" in urn else f"Resource{i}"
        
        # Clean up resource name for diagram
        clean_name = resource_name.replace("-", "_").replace(".", "_")
        style = get_resource_type_style(resource_type)
        
        diagram += f"        {clean_name}[{resource_name}]:::{style}\n"
        resource_nodes[urn] = clean_name
    
    diagram += "    end\n"
    
    # Add basic relationships (this is simplified - real relationships would need dependency analysis)
    diagram += "\n    %% Add relationships based on your stack's actual dependencies\n"
    diagram += "    %% Example: ResourceA --> ResourceB\n"
    
    diagram += "```\n\n"
    
    # Add resource list
    diagram += "## Resources\n"
    for resource in resources:
        if resource.get("type") == "pulumi:pulumi:Stack":
            continue
        resource_type = resource.get("type", "")
        urn = resource.get("urn", "")
        resource_name = urn.split("::")[-1] if "::" in urn else "Unknown"
        diagram += f"- **{resource_name}** ({resource_type})\n"
    
    return diagram

def main():
    parser = argparse.ArgumentParser(description="Generate architecture diagram from Pulumi stack")
    parser.add_argument("stack_name", help="Name of the Pulumi stack")
    parser.add_argument("--project", help="Pulumi project directory")
    parser.add_argument("--org", help="Pulumi organization")
    
    args = parser.parse_args()
    
    # Export stack
    stack_export = get_stack_export(args.stack_name, args.project, args.org)
    if not stack_export:
        sys.exit(1)
    
    # Generate diagram
    diagram_content = generate_mermaid_diagram(stack_export, args.stack_name)
    
    # Write to file
    output_path = Path("stacks") / f"{args.stack_name}.md"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(diagram_content)
    
    print(f"Generated diagram: {output_path}")

if __name__ == "__main__":
    main()