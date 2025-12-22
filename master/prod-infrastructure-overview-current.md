# Production Infrastructure Overview - Current State

This diagram shows the complete production infrastructure architecture across all Pulumi stacks.

```mermaid
graph TB
    subgraph "Production Environment - AWS us-east-1"
        subgraph "server-infra Stack"
            subgraph "VPC: acme-vpc (10.0.0.0/16)"
                subgraph "Availability Zone: us-east-1a"
                    SUBNET[Public Subnet<br/>10.0.1.0/24<br/>subnet-0d2cc4a0428e74929]
                    
                    SERVER[EC2 Instance<br/>acme-server<br/>t3.small<br/>18.208.207.234]
                end

                VPC[VPC<br/>acme-vpc<br/>10.0.0.0/16]
                IGW[Internet Gateway<br/>acme-igw]
                RT[Route Table<br/>acme-route-table]
                SG[Security Group<br/>acme-security-group]
            end
        end
    end

    INTERNET((Internet<br/>External Users))
    SSH_ADMIN((SSH Admin<br/>24.118.202.3))

    %% Network Architecture
    INTERNET ---|Public Access| IGW
    IGW ---|Attached to| VPC
    VPC ---|Contains| SUBNET
    SUBNET ---|Hosts| SERVER
    RT ---|Routes 0.0.0.0/0 to| IGW
    SUBNET ---|Associated with| RT
    SG ---|Protects| SERVER

    %% Traffic Flows
    INTERNET ..->|HTTP:80<br/>HTTPS:443| SERVER
    SSH_ADMIN ..->|SSH:22| SERVER
    SERVER ..->|All Outbound| INTERNET

    %% Security Boundaries
    SG -.->|Ingress Rules:<br/>HTTP:80 (0.0.0.0/0)<br/>HTTPS:443 (0.0.0.0/0)<br/>SSH:22 (24.118.202.3/32)| SERVER
    SG -.->|Egress Rules:<br/>All traffic (0.0.0.0/0)| INTERNET

    %% Styling
    classDef stack fill:#146EB4,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef vpc fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef subnet fill:#3F48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef compute fill:#FF9900,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef gateway fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef security fill:#DD344C,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef routing fill:#8C4FFF,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef external fill:#879196,stroke:#232F3E,stroke-width:2px,color:#fff

    class VPC vpc
    class SUBNET subnet
    class SERVER compute
    class IGW gateway
    class SG security
    class RT routing
    class INTERNET,SSH_ADMIN external
```

## Infrastructure Summary

### Production Stacks

Currently, there is **1 production stack** deployed:

1. **server-infra (prod)**: ACME server infrastructure with networking and compute resources

### Resource Count

- **Total Resources**: 10 managed resources
  - 1 VPC
  - 1 Subnet
  - 1 Internet Gateway
  - 1 Route Table
  - 1 Route
  - 1 Route Table Association
  - 1 Security Group
  - 1 EC2 Instance
  - 1 AWS Provider
  - 1 Stack Resource

### Cloud Provider

- **Provider**: AWS
- **Region**: us-east-1
- **Account**: 052848974346

## Architecture Overview

### Network Architecture

The production environment consists of a single VPC with a simple public subnet architecture:

- **VPC CIDR**: 10.0.0.0/16
- **Public Subnet CIDR**: 10.0.1.0/24 (us-east-1a)
- **Internet Connectivity**: Direct via Internet Gateway
- **Routing**: All internet-bound traffic (0.0.0.0/0) routes through the Internet Gateway

### Compute Resources

- **EC2 Instance**: Single t3.small instance running the ACME server
  - Public IP: 18.208.207.234
  - Private IP: 10.0.1.78
  - Key Pair: elisabeth-key-pair
  - State: running

### Security Configuration

#### Network Security

- **Security Group**: acme-security-group
  - **Inbound**:
    - SSH (port 22): Restricted to 24.118.202.3/32
    - HTTP (port 80): Open to internet (0.0.0.0/0) for ACME HTTP-01 challenges
    - HTTPS (port 443): Open to internet (0.0.0.0/0) for ACME protocol
  - **Outbound**:
    - All traffic: Allowed to internet (0.0.0.0/0)

#### Access Control

- **SSH Access**: Restricted to a single IP address for administrative access
- **Public Services**: HTTP and HTTPS are publicly accessible for ACME operations

## Data Flow Patterns

### Inbound Traffic Flow

```
Internet → Internet Gateway → Route Table → Public Subnet → Security Group → EC2 Instance
```

1. External users/services connect to the public IP (18.208.207.234)
2. Traffic passes through the Internet Gateway
3. Route table directs traffic to the public subnet
4. Security group filters traffic based on protocol and source
5. Allowed traffic reaches the EC2 instance

### Outbound Traffic Flow

```
EC2 Instance → Security Group → Public Subnet → Route Table → Internet Gateway → Internet
```

1. EC2 instance initiates outbound connections
2. Security group allows all outbound traffic
3. Route table directs traffic to the Internet Gateway
4. Traffic exits to the internet

## Cross-Stack Dependencies

Currently, there are **no cross-stack dependencies** as only one stack exists in production.

### Future Considerations

If additional stacks are added, consider:
- Exporting VPC ID, Subnet ID, and Security Group ID as stack outputs
- Creating separate stacks for different concerns (networking, compute, monitoring)
- Implementing cross-stack references for shared resources

## Operational Characteristics

### High Availability

- **Current State**: Single availability zone deployment
- **Risk**: No redundancy or failover capability
- **Recommendation**: Consider multi-AZ deployment for production workloads

### Scalability

- **Current State**: Single EC2 instance
- **Capacity**: t3.small (2 vCPUs, 2 GB RAM, burstable)
- **Recommendation**: Consider Auto Scaling Group or containerization for horizontal scaling

### Security Posture

- **Strengths**:
  - SSH access properly restricted to single IP
  - Security group follows principle of least privilege for inbound traffic
  - All resources properly tagged
  
- **Considerations**:
  - Instance is directly exposed to internet
  - No WAF or DDoS protection
  - Consider adding CloudWatch monitoring and alarms

### Cost Optimization

- **Instance Type**: t3.small with unlimited CPU credits
- **Network**: Standard data transfer rates apply
- **Estimated Monthly Cost**: ~$15-20 for compute + data transfer

## Monitoring and Observability

### Current State

- No CloudWatch Logs integration visible in stack
- No CloudWatch Alarms configured
- No centralized logging solution

### Recommendations

- Add CloudWatch agent to EC2 instance
- Configure CloudWatch Alarms for:
  - CPU utilization
  - Network traffic anomalies
  - Instance health checks
- Implement centralized logging (CloudWatch Logs or third-party solution)

## Compliance and Governance

### Tagging Strategy

All resources follow a consistent naming convention with the `acme-` prefix:
- acme-vpc
- acme-public-subnet
- acme-igw
- acme-route-table
- acme-security-group
- acme-server

### Resource Naming

Resources use Pulumi's auto-naming feature with logical names, ensuring:
- No naming conflicts
- Easy identification in AWS console
- Consistent naming patterns

## Future Architecture Considerations

### Potential Enhancements

1. **High Availability**:
   - Deploy across multiple availability zones
   - Implement Application Load Balancer
   - Add Auto Scaling Group

2. **Security**:
   - Add AWS WAF for web application firewall
   - Implement AWS Shield for DDoS protection
   - Use AWS Systems Manager Session Manager instead of direct SSH

3. **Monitoring**:
   - Add CloudWatch Logs and Metrics
   - Implement CloudWatch Alarms
   - Consider third-party monitoring (Datadog, New Relic)

4. **Infrastructure Organization**:
   - Split into multiple stacks (network, compute, monitoring)
   - Implement stack outputs for cross-stack references
   - Add separate stacks for different environments (dev, staging, prod)

5. **Disaster Recovery**:
   - Implement automated backups (EBS snapshots, AMI creation)
   - Document recovery procedures
   - Test failover scenarios

## Stack Details

### server-infra Stack

- **Project**: server-infra
- **Stack**: prod
- **Resources**: 10 managed resources
- **Provider**: AWS (version 7.14.0)
- **Region**: us-east-1
- **Purpose**: ACME server infrastructure with networking and compute

For detailed resource information, see [server-infra-prod.md](../stacks/server-infra-prod.md)
