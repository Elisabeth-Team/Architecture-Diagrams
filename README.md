# Architecture Diagrams

This repository contains architecture diagrams for all production infrastructure managed by Pulumi.

## Structure

```
├── stacks/           # Individual stack diagrams
├── master/           # Master overview diagrams
├── templates/        # Template files for new diagrams
└── scripts/          # Automation scripts
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

### Cloud Provider Icons & Colors
- **AWS resources**: `#FF9900` (orange) with service-specific icons
  - 🔑 IAM roles and security
  - 🌐 VPC and networking
  - 🐳 ECS and containers
  - 💾 S3 and storage
  - 📊 CloudWatch and monitoring
- **GCP resources**: `#4285F4` (blue) with service-specific icons
- **Azure resources**: `#0078D4` (blue) with service-specific icons
- **Kubernetes**: `#326CE5` (blue) with ⚙️ icons
- **Stack References**: `#9C27B0` (purple) with 🔗 icons
- **External/Internet**: `#28A745` (green) with 🌍 icons

### Icon Standards
Use Unicode emojis to represent different resource types:
- 🔑 IAM roles and security
- 🌐 VPC, networking
- 🐳 Containers, ECS
- 💾 Storage (S3, databases)
- 📊 Monitoring, logs
- 🔗 Stack references
- 🌍 Internet, external services

## Updating Diagrams

1. When infrastructure changes, update the corresponding stack diagram
2. Update the master overview if new stacks are added or relationships change
3. Use the templates in `templates/` for consistency
4. Validate Mermaid syntax before committing

## Automation

The `scripts/` directory contains tools to help maintain diagrams:

- `validate-diagrams.py` - Validate all Mermaid syntax
