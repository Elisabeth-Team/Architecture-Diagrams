# Current Production Infrastructure - December 2024

This document provides a summary of the current production infrastructure as of the latest update.

## Quick Links

- **Complete Overview**: [prod-infrastructure-complete-overview.md](master/prod-infrastructure-complete-overview.md)
- **IAM Stack**: [iam-infrastructure-iaminfra.md](stacks/iam-infrastructure-iaminfra.md)
- **Network Stack**: [network-infrastructure-networkstack.md](stacks/network-infrastructure-networkstack.md)
- **Server Stack**: [server-infra-prod.md](stacks/server-infra-prod.md)

## Production Stacks

### Deployed Stacks

| Stack Name | Project | Resources | Purpose | Region | Repository |
|------------|---------|-----------|---------|--------|------------|
| iaminfra | iam-infrastructure | 8 | IAM roles for ECS | us-east-1 | lichtie/prod-infrastructure |
| networkstack | network-infrastructure | 8 | ECS networking | us-east-1 | lichtie/prod-infrastructure |
| prod | server-infra | 10 | ACME server | us-east-1 | (standalone) |

**Total**: 26 managed resources across 3 deployed stacks

### Stack Details

#### iam-infrastructure/iaminfra

**Purpose**: IAM roles and policies for ECS operations

**Key Resources**:
- 3 IAM Roles (ECS cluster, instance, and task execution)
- 3 IAM Role Policies (attached to roles)
- 1 AWS Provider
- 1 Stack Resource

**Exports**:
- ecsClusterRoleArn: arn:aws:iam::052848974346:role/ecsClusterRole-5e1a580
- ecsInstanceRoleArn: arn:aws:iam::052848974346:role/ecsInstanceRole-51fe46e
- frontendServiceRoleArn: arn:aws:iam::052848974346:role/frontendServiceRole-989c78a

**Status**: ✅ Deployed and ready for ECS cluster

#### network-infrastructure/networkstack

**Purpose**: Networking infrastructure for ECS workloads

**Key Resources**:
- 1 VPC (10.0.0.0/16)
- 1 Public Subnet (10.0.1.0/24) in us-east-1a
- 1 Internet Gateway
- 1 Route Table with internet route
- 1 Route Table Association
- 1 Security Group (HTTP, SSH)

**Exports**:
- vpcId: vpc-05d6664f26f91261b
- publicSubnetId: subnet-05b39df7a84c55aff
- securityGroupId: sg-0d52a1c384768365e

**Status**: ✅ Deployed and ready for ECS cluster

#### server-infra/prod

**Purpose**: ACME server infrastructure

**Key Resources**:
- 1 VPC (10.0.0.0/16)
- 1 Public Subnet (10.0.1.0/24) in us-east-1a
- 1 Internet Gateway
- 1 Route Table with internet route
- 1 Route Table Association
- 1 Security Group (SSH, HTTP, HTTPS)
- 1 EC2 Instance (t3.small, running)

**Public Endpoints**:
- EC2 Instance: 18.208.207.234
- Public DNS: ec2-18-208-207-234.compute-1.amazonaws.com

**Status**: ✅ Deployed and operational

### Planned But Not Deployed

#### ecs-cluster

**Purpose**: ECS Fargate cluster with containerized workloads

**Planned Resources**:
- ECS Cluster
- CloudWatch Log Group
- ECS Task Definition (nginx container)
- ECS Service

**Status**: ❌ Code exists in repository but not deployed

**Dependencies**: Would reference iam-infrastructure and network-infrastructure stacks

## Infrastructure Topology

### ECS Foundation (Prepared, Not Active)

```
IAM Roles (iaminfra)
    ↓
VPC: ecs-vpc (10.0.0.0/16) (networkstack)
    ↓
Public Subnet (10.0.1.0/24, us-east-1a)
    ↓
Internet Gateway
    ↓
[ECS Cluster would be deployed here]
```

### ACME Server (Active)

```
Internet
   ↓
Internet Gateway (acme-igw)
   ↓
VPC: acme-vpc (10.0.0.0/16)
   ↓
Public Subnet (10.0.1.0/24, us-east-1a)
   ↓
EC2 Instance: acme-server (t3.small)
   - Public IP: 18.208.207.234
   - Private IP: 10.0.1.78
   - Security Group: acme-security-group
```

## Resource Summary

### By Service Type

| Service | Count | Stacks |
|---------|-------|--------|
| VPC | 2 | network-infrastructure, server-infra |
| Subnet | 2 | network-infrastructure, server-infra |
| Internet Gateway | 2 | network-infrastructure, server-infra |
| Route Table | 2 | network-infrastructure, server-infra |
| Security Group | 2 | network-infrastructure, server-infra |
| EC2 Instance | 1 | server-infra |
| IAM Role | 3 | iam-infrastructure |
| IAM Role Policy | 3 | iam-infrastructure |

### By Stack

| Stack | Resources | Key Services |
|-------|-----------|--------------|
| iam-infrastructure/iaminfra | 8 | IAM Roles, IAM Policies |
| network-infrastructure/networkstack | 8 | VPC, Subnet, IGW, Route Table, Security Group |
| server-infra/prod | 10 | VPC, Subnet, IGW, Route Table, Security Group, EC2 |

## Network Architecture

### ECS Infrastructure Network (ecs-vpc)

- **VPC ID**: vpc-05d6664f26f91261b
- **VPC CIDR**: 10.0.0.0/16
- **DNS Support**: Enabled
- **DNS Hostnames**: Enabled
- **Subnet**: 10.0.1.0/24 (us-east-1a)
- **Internet Gateway**: igw-0376448381106889d
- **Security Group**: sg-0d52a1c384768365e

**Purpose**: Ready to host ECS Fargate tasks

### ACME Server Network (acme-vpc)

- **VPC ID**: vpc-0c279b384c53c9a54
- **VPC CIDR**: 10.0.0.0/16
- **DNS Support**: Enabled
- **DNS Hostnames**: Enabled
- **Subnet**: 10.0.1.0/24 (us-east-1a)
- **Internet Gateway**: igw-00d4ccff6095c3df0
- **Security Group**: sg-011d50c294de77339

**Purpose**: Hosts ACME server EC2 instance

### Network Isolation

The two infrastructure groups use **separate VPCs** with no peering:
- ECS infrastructure: vpc-05d6664f26f91261b
- ACME server: vpc-0c279b384c53c9a54

## Security Configuration

### IAM Roles

| Role | ARN | Purpose |
|------|-----|---------|
| ecsClusterRole | arn:aws:iam::052848974346:role/ecsClusterRole-5e1a580 | ECS cluster management |
| ecsInstanceRole | arn:aws:iam::052848974346:role/ecsInstanceRole-51fe46e | EC2 instance ECS agent |
| frontendServiceRole | arn:aws:iam::052848974346:role/frontendServiceRole-989c78a | ECS task execution |

### Security Groups

#### ECS Security Group (sg-0d52a1c384768365e)

**Inbound Rules**:
| Protocol | Port | Source | Description |
|----------|------|--------|-------------|
| TCP | 80 | 0.0.0.0/0 | HTTP |
| TCP | 22 | 0.0.0.0/0 | SSH ⚠️ Broad access |

**Outbound Rules**:
| Protocol | Port | Destination | Description |
|----------|------|-------------|-------------|
| All | All | 0.0.0.0/0 | Allow all outbound |

#### ACME Security Group (sg-011d50c294de77339)

**Inbound Rules**:
| Protocol | Port | Source | Description |
|----------|------|--------|-------------|
| TCP | 22 | 24.118.202.3/32 | SSH ✅ Restricted |
| TCP | 80 | 0.0.0.0/0 | HTTP for ACME |
| TCP | 443 | 0.0.0.0/0 | HTTPS for ACME |

**Outbound Rules**:
| Protocol | Port | Destination | Description |
|----------|------|-------------|-------------|
| All | All | 0.0.0.0/0 | Allow all outbound |

## Compute Resources

### Active Compute

| Name | Instance ID | Type | State | AZ | Private IP | Public IP |
|------|-------------|------|-------|----|-----------|-----------| 
| acme-server | i-0a1b95317e253417a | t3.small | running | us-east-1a | 10.0.1.78 | 18.208.207.234 |

**Instance Details**:
- **AMI**: ami-0030e4319cbf4dbf2
- **vCPUs**: 2 (burstable)
- **Memory**: 2 GB
- **Storage**: 20 GB gp3
- **Key Pair**: elisabeth-key-pair

### Planned Compute (Not Deployed)

| Resource | Type | Configuration | Status |
|----------|------|---------------|--------|
| ECS Cluster | Fargate | my-ecs-cluster | Not deployed |
| Frontend Task | Fargate | nginx, 256 CPU, 512 MB | Not deployed |

## Cross-Stack Dependencies

### Active Dependencies

Currently **no active cross-stack dependencies** because:
- ACME server is standalone
- ECS cluster is not deployed

### Prepared Dependencies

When ECS cluster is deployed, it will reference:
- **iam-infrastructure/iaminfra**: frontendServiceRoleArn
- **network-infrastructure/networkstack**: publicSubnetId, securityGroupId

## Operational Characteristics

### High Availability

| Component | Current State | Recommendation |
|-----------|---------------|----------------|
| ACME Server | ❌ Single AZ | Multi-AZ or Auto Scaling |
| ECS Infrastructure | ❌ Single AZ | Deploy across multiple AZs |
| IAM Roles | ✅ Regional | No action needed |

### Monitoring

| Stack | CloudWatch Logs | CloudWatch Alarms | Status |
|-------|-----------------|-------------------|--------|
| server-infra | ❌ Not configured | ❌ Not configured | Needs monitoring |
| network-infrastructure | N/A | N/A | No compute |
| iam-infrastructure | N/A | N/A | Use CloudTrail |

### Backup & Recovery

| Component | Automated Backups | Snapshots | DR Plan |
|-----------|-------------------|-----------|---------|
| ACME Server | ❌ Not configured | ❌ Not configured | ❌ Not documented |
| ECS Infrastructure | N/A | N/A | N/A |

## Cost Estimation

### Current Monthly Costs (Approximate)

| Component | Configuration | Estimated Cost |
|-----------|--------------|----------------|
| ACME Server EC2 | t3.small (730 hrs) | ~$15.18 |
| ACME Server EBS | 20 GB gp3 | ~$1.60 |
| ECS Infrastructure | No compute running | $0 |
| IAM Roles | No charge | $0 |
| Data Transfer | Varies | ~$0-10 |
| **Total** | | **~$17-27/month** |

### When ECS Cluster is Deployed (Additional)

| Component | Configuration | Estimated Cost |
|-----------|--------------|----------------|
| Fargate Task | 256 CPU, 512 MB, 1 task | ~$10-15 |
| CloudWatch Logs | 14-day retention | ~$1-5 |
| **Additional Total** | | **~$11-20/month** |

## Compliance & Governance

### Tagging

**ECS Infrastructure** (ecs- prefix):
- ✅ ecs-vpc, ecs-public-subnet, ecs-igw, ecs-route-table, ecs-security-group

**ACME Server** (acme- prefix):
- ✅ acme-vpc, acme-public-subnet, acme-igw, acme-route-table, acme-security-group, acme-server

### Resource Naming

- ✅ Consistent naming within each infrastructure group
- ✅ Pulumi auto-naming for physical resources
- ✅ Descriptive logical names

## Known Limitations

### ACME Server

1. **Single Point of Failure**: Instance in single AZ with no redundancy
2. **No Load Balancing**: Direct instance exposure
3. **Limited Monitoring**: No CloudWatch Logs or alarms
4. **No Backup Strategy**: No automated backups
5. **Public Exposure**: Direct internet access

### ECS Infrastructure

1. **Not Deployed**: Infrastructure ready but cluster not deployed
2. **Single AZ**: Subnet in single availability zone
3. **Broad SSH Access**: Security group allows SSH from 0.0.0.0/0
4. **No Monitoring**: No CloudWatch Logs configured

## Recommendations

### High Priority

1. **Deploy ECS Cluster**: Infrastructure is ready, deploy the ecs-cluster stack
2. **Restrict SSH Access**: Update ECS security group to restrict SSH
3. **Add Monitoring**: Implement CloudWatch Logs and Alarms for ACME server
4. **Backup Strategy**: Configure automated EBS snapshots

### Medium Priority

1. **Multi-AZ Deployment**: Deploy both infrastructures across multiple AZs
2. **Load Balancers**: Add ALBs for both ECS and ACME server
3. **Documentation**: Document operational procedures
4. **Cost Optimization**: Review instance sizing

### Low Priority

1. **VPC Consolidation**: Evaluate if both VPCs are needed
2. **WAF/Shield**: Add DDoS protection
3. **Systems Manager**: Use Session Manager instead of SSH
4. **Service Mesh**: Consider AWS App Mesh for ECS

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2024-12-XX | Initial documentation of complete production infrastructure | Pulumi Neo |

## Related Documentation

- [Complete Overview Diagram](master/prod-infrastructure-complete-overview.md)
- [IAM Stack Diagram](stacks/iam-infrastructure-iaminfra.md)
- [Network Stack Diagram](stacks/network-infrastructure-networkstack.md)
- [Server Stack Diagram](stacks/server-infra-prod.md)
- [Visual Standards](VISUAL_STANDARDS.md)
- [Update Procedures](UPDATE_PROCEDURES.md)
