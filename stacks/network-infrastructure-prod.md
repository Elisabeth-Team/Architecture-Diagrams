# Network Infrastructure Stack - Production

This diagram shows the network infrastructure resources deployed in the `network-infrastructure` prod stack.

```mermaid
graph TB
    subgraph "AWS Region: us-east-1"
        subgraph "VPC: ecs-vpc (10.0.0.0/16)"
            VPC[VPC<br/>vpc-0c14c65de928961e3<br/>10.0.0.0/16]
            
            subgraph "Availability Zone: us-east-1b"
                SUBNET[Public Subnet<br/>subnet-01d1c207006d52e59<br/>10.0.1.0/24]
            end
            
            IGW[Internet Gateway<br/>igw-08fbc3e9c0a7e57fd]
            RT[Route Table<br/>rtb-0f5f08fe751ed9044]
            SG[Security Group<br/>sg-011d6da5dcd69ec9f<br/>ecs-security-group]
        end
    end
    
    INTERNET((Internet))
    
    %% Connections
    INTERNET ---|Public Access| IGW
    IGW ---|Attached to| VPC
    VPC ---|Contains| SUBNET
    RT ---|Routes 0.0.0.0/0 to| IGW
    SUBNET ---|Associated with| RT
    SG ---|Protects resources in| VPC
    
    %% Security Group Rules
    SG -.->|Ingress: HTTP (80)| INTERNET
    SG -.->|Ingress: SSH (22)| INTERNET
    SG -.->|Egress: All traffic| INTERNET
    
    %% Stack Outputs (exported to other stacks)
    SUBNET -.->|publicSubnetId| OUTPUTS[Stack Outputs]
    VPC -.->|vpcId| OUTPUTS
    SG -.->|securityGroupId| OUTPUTS
    
    %% Styling
    classDef vpc fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef subnet fill:#3F48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef gateway fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef security fill:#DD344C,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef routing fill:#8C4FFF,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef outputs fill:#146EB4,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class VPC vpc
    class SUBNET subnet
    class IGW gateway
    class SG security
    class RT routing
    class OUTPUTS outputs
```

## Resources Summary

### Core Network Components
- **VPC**: `vpc-0c14c65de928961e3` (10.0.0.0/16)
- **Public Subnet**: `subnet-01d1c207006d52e59` (10.0.1.0/24) in us-east-1b
- **Internet Gateway**: `igw-08fbc3e9c0a7e57fd`
- **Route Table**: `rtb-0f5f08fe751ed9044`
- **Security Group**: `sg-011d6da5dcd69ec9f`

### Security Configuration
- **Ingress Rules**: HTTP (port 80) and SSH (port 22) from anywhere (0.0.0.0/0)
- **Egress Rules**: All traffic allowed to anywhere

### Stack Exports
This stack exports the following outputs for use by other stacks:
- `vpcId`: VPC identifier
- `publicSubnetId`: Public subnet identifier  
- `securityGroupId`: Security group identifier

## Dependencies
- **Consumed by**: `cluster-infrastructure` stack (for ECS deployment)