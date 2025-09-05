# Architecture Diagrams

This repository contains architecture diagrams for all production infrastructure managed by Pulumi.

## Structure

```
├── stacks/           # Individual stack diagrams
├── master/           # Master overview diagrams
├── images/           # Auto-generated PNG images
│   ├── stacks/       # PNG versions of stack diagrams
│   └── master/       # PNG versions of master diagrams
├── templates/        # Template files for new diagrams
├── scripts/          # Automation scripts
└── .github/workflows/ # CI/CD automation
```

## Diagram Standards

### Individual Stack Diagrams
- One diagram per stack in the `stacks/` directory
- Named as `{stack-name}.md` containing Mermaid diagrams
- Include all resources, their relationships, and key configurations
- Show external dependencies and integrations

### Master Overview Diagram
- Located in `master/overview.md`
- Shows high-level architecture across all prod stacks
- Highlights StackReferences and inter-stack dependencies
- Groups related stacks and shows data flow

## Mermaid Conventions

- Use consistent colors and shapes for resource types
- AWS resources: `#FF9900` (orange)
- GCP resources: `#4285F4` (blue) 
- Azure resources: `#0078D4` (blue)
- Kubernetes: `#326CE5` (blue)
- Databases: `#336791` (dark blue)
- Load balancers: `#28A745` (green)
- Storage: `#FFC107` (yellow)

## Updating Diagrams

1. When infrastructure changes, update the corresponding stack diagram
2. Update the master overview if new stacks are added or relationships change
3. Use the templates in `templates/` for consistency
4. Validate Mermaid syntax before committing

## Automation

### Scripts
The `scripts/` directory contains tools to help maintain diagrams:
- `generate-stack-diagram.py` - Generate diagram from Pulumi stack export
- `validate-diagrams.py` - Validate all Mermaid syntax
- `update-master.py` - Update master overview from individual stack diagrams

### GitHub Actions
Automated workflows handle diagram maintenance:

#### PNG Generation (`generate-diagrams.yml`)
- **Triggers**: Push to main or PR with diagram changes
- **Actions**: 
  - Validates Mermaid syntax
  - Generates high-quality PNG images from all diagrams
  - Commits PNGs to `images/` directory on main branch
  - Uploads PNGs as artifacts for PRs
- **Image specs**: 1200x800px (stacks), 1400x1000px (master), white background

#### Validation (`validate-diagrams.yml`)
- **Triggers**: Push/PR to main/develop branches
- **Actions**:
  - Validates all Mermaid diagram syntax
  - Tests diagram rendering
  - Checks for common syntax errors

### Usage Examples

**Generate diagrams locally:**
```bash
python scripts/generate-stack-diagram.py my-stack-name
python scripts/update-master.py
python scripts/validate-diagrams.py
```

**Access PNG images:**
- Stack diagrams: `images/stacks/{stack-name}.png`
- Master overview: `images/master/overview.png`
- Images are auto-generated on every diagram update