# Diagram Update Procedures

This document outlines the procedures for keeping infrastructure diagrams synchronized with Pulumi state changes.

## Overview

Infrastructure diagrams must be kept current with the actual deployed infrastructure. This document provides procedures for:
- Detecting when updates are needed
- Updating diagrams systematically  
- Validating diagram accuracy
- Automating update processes

## Update Triggers

### Automatic Triggers
Diagrams should be updated automatically when:
- Pulumi deployments complete successfully
- New resources are added to stacks
- Resource configurations change
- Cross-stack dependencies are modified

### Manual Review Triggers
Manual review and updates are needed when:
- Security configurations change
- Network topology is modified
- New stacks are created or removed
- Major architectural changes occur

## Update Process

### 1. Detect Changes

#### Using Pulumi Resource Search
```bash
# Search for resources in specific stack
pulumi resource search "stack:prod project:network-infrastructure"

# Search for new resource types
pulumi resource search "type:aws:ec2/instance:Instance"

# Find cross-stack references
pulumi resource search "type:StackReference"
```

#### Using Pulumi CLI (if available)
```bash
# List stack resources
pulumi stack --stack prod export

# Show resource details
pulumi stack --stack prod output --json
```

### 2. Identify Affected Diagrams

#### Stack-Level Changes
- **IAM changes** → Update `iam-infrastructure-prod.md`
- **Network changes** → Update `network-infrastructure-prod.md`  
- **Cluster changes** → Update `cluster-infrastructure-prod.md`
- **Cross-stack changes** → Update master overview diagram

#### Resource Type Mapping
| Resource Type | Affected Diagrams |
|---------------|-------------------|
| `aws:iam/role:Role` | IAM stack + Master overview |
| `aws:ec2/vpc:Vpc` | Network stack + Master overview |
| `aws:ecs/cluster:Cluster` | Cluster stack + Master overview |
| `pulumi:pulumi:StackReference` | All dependent stacks + Master |

### 3. Update Diagrams

#### Step-by-Step Process
1. **Clone the Architecture-Diagrams repository**
2. **Gather current infrastructure state** using Pulumi resource search
3. **Compare with existing diagrams** to identify differences
4. **Update affected diagram files** following visual standards
5. **Validate diagram syntax** using provided scripts
6. **Test diagram rendering** in Mermaid preview
7. **Commit changes** with descriptive messages

#### Example Update Workflow
```bash
# 1. Clone repository
git clone https://github.com/Elisabeth-Team/Architecture-Diagrams.git
cd Architecture-Diagrams

# 2. Create feature branch
git checkout -b update-prod-diagrams-$(date +%Y%m%d)

# 3. Update diagrams (manual process)
# Edit relevant .md files in /stacks/ and /master/

# 4. Validate changes
python scripts/validate-diagrams.py

# 5. Commit and push
git add .
git commit -m "Update prod infrastructure diagrams - added new ECS service"
git push origin update-prod-diagrams-$(date +%Y%m%d)

# 6. Create pull request
```

### 4. Validation Steps

#### Syntax Validation
```bash
# Run validation script
python scripts/validate-diagrams.py

# Check specific file
python scripts/validate-diagrams.py stacks/cluster-infrastructure-prod.md
```

#### Content Validation Checklist
- [ ] All resource IDs match current infrastructure
- [ ] Cross-stack references are accurate
- [ ] Security group rules reflect current configuration
- [ ] Network topology matches deployed state
- [ ] IAM roles and policies are current
- [ ] Container configurations match task definitions

#### Visual Validation
- [ ] Diagram renders correctly in Mermaid
- [ ] All connections are labeled appropriately
- [ ] Color scheme follows visual standards
- [ ] Node groupings are logical and clear
- [ ] No overlapping or unclear elements

## Automation Strategies

### CI/CD Integration

#### GitHub Actions Workflow
```yaml
name: Update Infrastructure Diagrams
on:
  repository_dispatch:
    types: [pulumi-deployment-complete]
  
jobs:
  update-diagrams:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Query Pulumi Resources
        run: |
          # Use Pulumi API to get current state
          # Compare with existing diagrams
          # Generate updates if needed
      - name: Validate Diagrams
        run: python scripts/validate-diagrams.py
      - name: Create Pull Request
        if: changes detected
        uses: peter-evans/create-pull-request@v4
```

#### Pulumi Hooks
```typescript
// In Pulumi program
import * as pulumi from "@pulumi/pulumi";

// Post-deployment hook
pulumi.runtime.registerStackTransformation((args) => {
    // Trigger diagram update webhook
    // Send resource changes to diagram service
    return args;
});
```

### Webhook Integration

#### Pulumi Cloud Webhooks
Configure webhooks in Pulumi Cloud to trigger updates:
- **Event**: Stack update completed
- **Target**: GitHub repository dispatch
- **Payload**: Stack name, resources changed, deployment status

#### Example Webhook Handler
```javascript
// Webhook endpoint to handle Pulumi events
app.post('/pulumi-webhook', (req, res) => {
    const { stack, resources, status } = req.body;
    
    if (status === 'succeeded') {
        // Trigger diagram update process
        triggerDiagramUpdate(stack, resources);
    }
    
    res.status(200).send('OK');
});
```

## Change Management

### Version Control Strategy

#### Branching Model
- **Main branch**: Production-ready diagrams
- **Feature branches**: Updates for specific changes
- **Release tags**: Major architecture milestones

#### Commit Message Format
```
type(scope): description

Examples:
feat(network): add new private subnet configuration
fix(iam): correct role permissions in diagram
update(cluster): reflect new ECS service deployment
docs(standards): update visual standards for GCP resources
```

### Review Process

#### Pull Request Requirements
- [ ] All affected diagrams updated
- [ ] Validation scripts pass
- [ ] Visual standards followed
- [ ] Change description provided
- [ ] Resource IDs verified

#### Review Checklist
- [ ] Technical accuracy verified
- [ ] Visual clarity maintained
- [ ] Documentation updated
- [ ] No sensitive information exposed
- [ ] Cross-references validated

## Monitoring & Maintenance

### Regular Audits

#### Monthly Reviews
- Compare diagrams with actual infrastructure
- Identify drift or outdated information
- Update resource configurations
- Review cross-stack dependencies

#### Quarterly Assessments
- Evaluate diagram effectiveness
- Update visual standards if needed
- Review automation processes
- Plan architectural documentation improvements

### Metrics & KPIs

#### Diagram Accuracy
- Percentage of resources correctly represented
- Time between infrastructure change and diagram update
- Number of outdated diagrams identified

#### Usage & Value
- Diagram view/access frequency
- User feedback on diagram usefulness
- Time saved in architecture discussions

### Troubleshooting

#### Common Issues

**Mermaid Syntax Errors**
- Use validation script before committing
- Check for special characters in labels
- Verify subgraph nesting structure

**Resource ID Mismatches**
- Query current Pulumi state
- Verify resource names haven't changed
- Check for resource replacements

**Cross-Stack Reference Errors**
- Validate stack outputs exist
- Check stack reference configurations
- Verify dependency relationships

**Rendering Issues**
- Test in multiple Mermaid renderers
- Simplify complex diagrams
- Check for circular references

## Tools & Scripts

### Validation Script
Location: `/scripts/validate-diagrams.py`
Purpose: Validate Mermaid syntax and check for common issues

### Update Helper Script
Location: `/scripts/update-helper.py`
Purpose: Assist with gathering current infrastructure state

### Diagram Generator
Location: `/scripts/generate-diagram.py`
Purpose: Auto-generate basic diagrams from Pulumi state

## Contact & Support

For questions about diagram updates or procedures:
- Create an issue in the Architecture-Diagrams repository
- Contact the platform engineering team
- Refer to visual standards documentation