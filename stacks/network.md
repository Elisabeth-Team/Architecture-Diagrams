# Network Stack Architecture

## Overview
The Network stack provides the foundational networking infrastructure for the production ECS environment. It creates a VPC with public subnets, internet connectivity, and security groups required for containerized workloads.

## Resources
Key resources deployed by this stack:
- **ecsVpc**: Main VPC with 10.0.0.0/16 CIDR block
- **ecsPublicSubnet**: Public subnet for ECS tasks
- **ecsInternetGateway**: Internet gateway for public connectivity
- **ecsRouteTable**: Route table with internet routing
- **ecsRouteTableAssociation**: Associates route table with subnet
- **ecsSecurityGroup**: Security group for ECS services

## Dependencies
- **Stack References**: None (foundational stack)
- **External Dependencies**: AWS VPC service, EC2 networking

## Architecture Diagram

```mermaid
graph TB
    %% Define styles
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef vpc fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef subnet fill:#7ED321,stroke:#5BA517,stroke-width:2px,color:#fff
    classDef gateway fill:#F5A623,stroke:#D4941E,stroke-width:2px,color:#fff
    classDef security fill:#D0021B,stroke:#A8001A,stroke-width:2px,color:#fff
    classDef route fill:#9013FE,stroke:#6A0DAD,stroke-width:2px,color:#fff
    
    subgraph "Stack: network"
        subgraph "VPC: 10.0.0.0/16"
            VPC[ecsVpc<br/>10.0.0.0/16]:::vpc
            
            subgraph "Public Subnet"
                SUBNET[ecsPublicSubnet<br/>Public Subnet]:::subnet
                SG[ecsSecurityGroup<br/>Security Group]:::security
            end
            
            subgraph "Internet Connectivity"
                IGW[ecsInternetGateway<br/>Internet Gateway]:::gateway
                RT[ecsRouteTable<br/>Route Table]:::route
                RTA[ecsRouteTableAssociation<br/>Route Association]:::route
            end
        end
        
        subgraph "AWS Provider"
            AWSP[AWS Provider us-east-1<br/>v6.13.3]:::aws
        end
    end
    
    subgraph "Internet"
        INTERNET[Internet<br/>0.0.0.0/0]:::gateway
    end
    
    %% VPC relationships
    VPC --> SUBNET
    VPC --> IGW
    VPC --> RT
    
    %% Subnet relationships
    SUBNET --> SG
    SUBNET --> RTA
    
    %% Routing relationships
    RT --> RTA
    RT --> IGW
    IGW --> INTERNET
    
    %% Provider relationships
    AWSP --> VPC
```

## Configuration
Key configuration values used by this stack:
- **AWS Region**: us-east-1
- **AWS Provider Version**: 6.13.3
- **VPC CIDR**: 10.0.0.0/16
- **DNS Support**: Enabled
- **DNS Hostnames**: Enabled

## Outputs
Key outputs that other stacks reference:
- **vpcId**: VPC identifier for resource placement
- **publicSubnetId**: Subnet for ECS task placement
- **securityGroupId**: Security group for ECS services

## Network Configuration

### VPC Details
- **CIDR Block**: 10.0.0.0/16 (65,536 IP addresses)
- **Instance Tenancy**: Default
- **DNS Resolution**: Enabled
- **DNS Hostnames**: Enabled

### Routing Configuration
- **Default Route**: 0.0.0.0/0 → Internet Gateway
- **Local Route**: 10.0.0.0/16 → Local (implicit)

### Security Groups
- **Default Security Group**: Created automatically
- **ECS Security Group**: Custom security group for ECS services

## Notes
This is a foundational networking stack that provides:
- Public internet connectivity for ECS Fargate tasks
- Secure network isolation through VPC
- Scalable subnet architecture ready for expansion
- Security group framework for service-level access control

The network is designed to support containerized workloads with public internet access, suitable for web applications and APIs.