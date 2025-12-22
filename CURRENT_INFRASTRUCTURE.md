# Current Production Infrastructure - December 2024

This document provides a summary of the current production infrastructure as of the latest update.

## Quick Links

- **Master Overview**: [prod-infrastructure-overview-current.md](master/prod-infrastructure-overview-current.md)
- **Stack Diagram**: [server-infra-prod.md](stacks/server-infra-prod.md)

## Production Stacks

### Active Stacks

| Stack Name | Project | Resources | Purpose | Region |
|------------|---------|-----------|---------|--------|
| prod | server-infra | 10 | ACME server infrastructure | us-east-1 |

### Stack Details

#### server-infra/prod

**Purpose**: ACME server infrastructure with networking and compute resources

**Key Resources**:
- 1 VPC (10.0.0.0/16)
- 1 Public Subnet (10.0.1.0/24) in us-east-1a
- 1 Internet Gateway
- 1 Route Table with internet route
- 1 Security Group (SSH, HTTP, HTTPS)
- 1 EC2 Instance (t3.small, running)

**Public Endpoints**:
- EC2 Instance: 18.208.207.234
- Public DNS: ec2-18-208-207-234.compute-1.amazonaws.com

**Security**:
- SSH restricted to 24.118.202.3/32
- HTTP/HTTPS open to internet for ACME operations
- All outbound traffic allowed

## Infrastructure Topology

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

| Service | Count | Resources |
|---------|-------|-----------|
| VPC | 1 | acme-vpc |
| Subnet | 1 | acme-public-subnet |
| Internet Gateway | 1 | acme-igw |
| Route Table | 1 | acme-route-table |
| Security Group | 1 | acme-security-group |
| EC2 Instance | 1 | acme-server |

### By Stack

| Stack | Resources | Services |
|-------|-----------|----------|
| server-infra/prod | 10 | VPC, Subnet, IGW, Route Table, Route, Route Table Association, Security Group, EC2, Provider, Stack |

## Network Architecture

### VPC Configuration

- **VPC CIDR**: 10.0.0.0/16
- **DNS Support**: Enabled
- **DNS Hostnames**: Enabled
- **Tenancy**: Default

### Subnet Configuration

- **Public Subnet**: 10.0.1.0/24
- **Availability Zone**: us-east-1a
- **Auto-assign Public IP**: Yes
- **Internet Access**: Via Internet Gateway

### Routing

- **Route Table**: acme-route-table
- **Routes**:
  - Local: 10.0.0.0/16 (implicit)
  - Internet: 0.0.0.0/0 → Internet Gateway

## Security Configuration

### Security Groups

#### acme-security-group

**Inbound Rules**:
| Protocol | Port | Source | Description |
|----------|------|--------|-------------|
| TCP | 22 | 24.118.202.3/32 | SSH access |
| TCP | 80 | 0.0.0.0/0 | HTTP for ACME HTTP-01 challenges |
| TCP | 443 | 0.0.0.0/0 | HTTPS for ACME protocol |

**Outbound Rules**:
| Protocol | Port | Destination | Description |
|----------|------|-------------|-------------|
| All | All | 0.0.0.0/0 | Allow all outbound traffic |

### Access Control

- **SSH Access**: Restricted to single IP (24.118.202.3)
- **HTTP/HTTPS**: Publicly accessible for ACME operations
- **Key Pair**: elisabeth-key-pair

## Compute Resources

### EC2 Instances

| Name | Instance ID | Type | State | AZ | Private IP | Public IP |
|------|-------------|------|-------|----|-----------|-----------| 
| acme-server | i-0a1b95317e253417a | t3.small | running | us-east-1a | 10.0.1.78 | 18.208.207.234 |

**Instance Details**:
- **AMI**: ami-0030e4319cbf4dbf2
- **vCPUs**: 2 (burstable)
- **Memory**: 2 GB
- **Storage**: 20 GB gp3 (3000 IOPS, 125 MB/s throughput)
- **CPU Credits**: Unlimited
- **Public DNS**: ec2-18-208-207-234.compute-1.amazonaws.com

## Operational Characteristics

### High Availability

- **Current State**: ❌ Single AZ deployment
- **Redundancy**: ❌ No redundancy
- **Failover**: ❌ No automatic failover

### Scalability

- **Horizontal Scaling**: ❌ Not configured
- **Vertical Scaling**: ✅ Manual instance type changes possible
- **Auto Scaling**: ❌ Not configured

### Monitoring

- **CloudWatch Metrics**: ✅ Default EC2 metrics
- **CloudWatch Logs**: ❌ Not configured
- **CloudWatch Alarms**: ❌ Not configured
- **Custom Monitoring**: ❌ Not configured

### Backup & Recovery

- **Automated Backups**: ❌ Not configured
- **Snapshots**: ❌ Not configured
- **Disaster Recovery Plan**: ❌ Not documented

## Cost Estimation

### Monthly Costs (Approximate)

| Service | Configuration | Estimated Cost |
|---------|--------------|----------------|
| EC2 Instance | t3.small (730 hrs/month) | ~$15.18 |
| EBS Storage | 20 GB gp3 | ~$1.60 |
| Data Transfer | Varies | ~$0-10 |
| **Total** | | **~$17-27/month** |

*Note: Costs are estimates and may vary based on actual usage, data transfer, and AWS pricing changes.*

## Compliance & Governance

### Tagging

All resources follow consistent naming with `acme-` prefix:
- ✅ VPC: acme-vpc
- ✅ Subnet: acme-public-subnet
- ✅ Internet Gateway: acme-igw
- ✅ Route Table: acme-route-table
- ✅ Security Group: acme-security-group
- ✅ EC2 Instance: acme-server

### Resource Naming

- ✅ Consistent naming convention
- ✅ Pulumi auto-naming for physical resources
- ✅ Descriptive logical names

## Known Limitations

1. **Single Point of Failure**: Instance in single AZ with no redundancy
2. **No Load Balancing**: Direct instance exposure without load balancer
3. **Limited Monitoring**: No CloudWatch Logs or custom alarms
4. **No Backup Strategy**: No automated backups or snapshots
5. **Public Exposure**: Instance directly accessible from internet
6. **No WAF/DDoS Protection**: No AWS WAF or Shield configured

## Recommendations

### High Priority

1. **Implement Monitoring**: Add CloudWatch Logs and Alarms
2. **Backup Strategy**: Configure automated EBS snapshots
3. **Documentation**: Document operational procedures and runbooks

### Medium Priority

1. **Multi-AZ Deployment**: Deploy across multiple availability zones
2. **Load Balancer**: Add Application Load Balancer for better availability
3. **Auto Scaling**: Implement Auto Scaling Group for resilience

### Low Priority

1. **WAF/Shield**: Add AWS WAF and Shield for DDoS protection
2. **Systems Manager**: Use Session Manager instead of direct SSH
3. **Cost Optimization**: Review instance sizing and reserved instances

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2024-12-XX | Initial documentation of current infrastructure | Pulumi Neo |

## Related Documentation

- [Visual Standards](VISUAL_STANDARDS.md)
- [Update Procedures](UPDATE_PROCEDURES.md)
- [Master Overview Diagram](master/prod-infrastructure-overview-current.md)
- [Stack Diagram](stacks/server-infra-prod.md)
