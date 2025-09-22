# Architecture Diagrams

This repository contains comprehensive architecture diagrams for all production infrastructure managed by Pulumi Infrastructure as Code.

## 📋 Current Infrastructure Coverage

### Production Environment
- **IAM Infrastructure Stack**: Identity and access management
- **Network Infrastructure Stack**: VPC, subnets, security groups, routing
- **Cluster Infrastructure Stack**: ECS clusters, services, and containerized applications

## 📁 Repository Structure

```
├── stacks/                    # Individual stack diagrams
│   ├── iam-infrastructure-prod.md
│   ├── network-infrastructure-prod.md
│   └── cluster-infrastructure-prod.md
├── master/                    # Master overview diagrams
│   └── prod-infrastructure-overview.md
├── templates/                 # Template files for new diagrams
│   ├── stack-template.md
│   └── master-template.md
├── scripts/                   # Automation and validation scripts
│   ├── validate-diagrams.py
│   ├── update-helper.py
│   └── generate-diagram.py
├── VISUAL_STANDARDS.md        # Comprehensive visual standards
├── UPDATE_PROCEDURES.md       # Diagram update procedures
└── README.md                  # This file
```

## 🎯 Diagram Types

### Individual Stack Diagrams (`/stacks/`)
- **Purpose**: Show resources within a single Pulumi stack
- **Scope**: Internal resource relationships and configurations
- **Naming**: `{stack-name}-{environment}.md`
- **Content**: Resources, dependencies, security configurations, exports

### Master Overview Diagrams (`/master/`)
- **Purpose**: Show complete system architecture and cross-stack dependencies
- **Scope**: Inter-stack relationships, data flow, and system boundaries
- **Naming**: `{environment}-infrastructure-overview.md`
- **Content**: Stack relationships, data flow patterns, security boundaries

## 🎨 Visual Standards

### Mermaid Diagram Standards
All diagrams use Mermaid syntax with consistent visual standards:

#### Color Scheme (AWS-Inspired)
- **IAM Resources**: Red (`#DD344C`) - Identity and access management
- **Network Resources**: Blue (`#3F48CC`) - VPC, subnets, routing
- **Compute Resources**: Orange (`#FF9900`) - ECS, EC2, containers
- **Container Resources**: Green (`#7AA116`) - Docker containers, tasks
- **AWS Services**: Purple (`#8C4FFF`) - Managed AWS services
- **Logging**: Dark Blue (`#146EB4`) - CloudWatch, log groups
- **External**: Gray (`#879196`) - Internet, external services
- **Outputs**: Dark Orange (`#FF6600`) - Stack outputs and references

#### Resource Representation
```mermaid
VPC[VPC<br/>vpc-0c14c65de928961e3<br/>10.0.0.0/16]
ROLE[IAM Role<br/>ecsInstanceRole-ee19158]
SERVICE[ECS Service<br/>frontendService-7ab8c00<br/>Desired: 1 task]
```

### Connection Types
- **Solid lines** (`---|Label|`): Direct resource relationships
- **Dashed lines** (`-.->|Label|`): Stack outputs/inputs, permissions
- **Dotted lines** (`..->|Protocol:Port|`): Network traffic flow

## 🔄 Keeping Diagrams Current

### When to Update
Diagrams should be updated when:
- ✅ New resources are added to stacks
- ✅ Resource configurations change significantly  
- ✅ Cross-stack dependencies are modified
- ✅ Security configurations are updated
- ✅ Network topology changes

### Update Process
1. **Detect Changes**: Use Pulumi resource search to identify infrastructure changes
2. **Update Diagrams**: Modify affected diagram files following visual standards
3. **Validate**: Run validation scripts to check syntax and accuracy
4. **Review**: Create pull request with clear change description
5. **Deploy**: Merge after review and validation

See [UPDATE_PROCEDURES.md](UPDATE_PROCEDURES.md) for detailed update procedures.

## 🛠 Tools & Automation

### Validation Scripts
```bash
# Validate all diagrams
python scripts/validate-diagrams.py

# Validate specific diagram
python scripts/validate-diagrams.py stacks/cluster-infrastructure-prod.md
```

### Helper Scripts
- **`update-helper.py`**: Assists with gathering current infrastructure state
- **`generate-diagram.py`**: Auto-generates basic diagrams from Pulumi state

### CI/CD Integration
- GitHub Actions workflow for automated validation
- Webhook integration with Pulumi Cloud for update triggers
- Pull request validation and review processes

## 📖 Documentation

### Comprehensive Guides
- **[VISUAL_STANDARDS.md](VISUAL_STANDARDS.md)**: Complete visual standards and conventions
- **[UPDATE_PROCEDURES.md](UPDATE_PROCEDURES.md)**: Detailed update and maintenance procedures

### Templates
- **[stack-template.md](templates/stack-template.md)**: Template for individual stack diagrams
- **[master-template.md](templates/master-template.md)**: Template for master overview diagrams

## 🚀 Quick Start

### Viewing Diagrams
1. Navigate to the appropriate directory (`/stacks/` or `/master/`)
2. Open the relevant `.md` file
3. View the Mermaid diagram in GitHub or your preferred Markdown renderer

### Creating New Diagrams
1. Use the appropriate template from `/templates/`
2. Follow the visual standards in `VISUAL_STANDARDS.md`
3. Validate using the provided scripts
4. Submit via pull request

### Updating Existing Diagrams
1. Follow the procedures in `UPDATE_PROCEDURES.md`
2. Use Pulumi resource search to gather current state
3. Update diagrams to reflect infrastructure changes
4. Validate and submit for review

## 🔍 Current Infrastructure Summary

### Production Environment Overview
- **AWS Account**: 052848974346
- **Region**: us-east-1
- **Stacks**: 3 (IAM, Network, Cluster)
- **Resources**: 25+ managed resources
- **Architecture**: Containerized web application on ECS Fargate

### Key Components
- **Networking**: VPC with public subnet and internet gateway
- **Compute**: ECS cluster running Nginx container on Fargate
- **Security**: IAM roles with least-privilege policies, security groups
- **Monitoring**: CloudWatch Logs with 14-day retention
- **Repository**: `github.com/lichtie/prod-infrastructure`

## 📞 Support & Contribution

### Getting Help
- Create an issue in this repository for diagram-related questions
- Contact the platform engineering team for infrastructure questions
- Refer to documentation for standards and procedures

### Contributing
1. Fork the repository
2. Create a feature branch
3. Follow visual standards and update procedures
4. Submit a pull request with clear description
5. Ensure all validation checks pass

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.