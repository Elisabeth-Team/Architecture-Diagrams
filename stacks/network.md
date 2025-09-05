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
    %% Define AWS service icon styles
    classDef awsNetwork fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef awsSecurity fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef internet fill:#28A745,stroke:#155724,stroke-width:2px,color:#fff

    subgraph "Stack: network"
        subgraph "🌐 VPC Infrastructure"
            VPC["🏢 ecsVpc<br/>10.0.0.0/16<br/>DNS: Enabled"]:::awsNetwork
            
            subgraph "🔗 Subnet Configuration"
                SUBNET["🌍 ecsPublicSubnet<br/>Public Subnet<br/>Auto-assign Public IP"]:::awsNetwork
            end
            
            subgraph "🛡️ Security"
                SG["🔒 ecsSecurityGroup<br/>ECS Security Group<br/>Ingress/Egress Rules"]:::awsSecurity
            end
        end

        subgraph "🚪 Internet Connectivity"
            IGW["🌐 ecsInternetGateway<br/>Internet Gateway<br/>Public Access"]:::awsNetwork
            RT["📋 ecsRouteTable<br/>Route Table<br/>0.0.0.0/0 → IGW"]:::awsNetwork
            RTA["🔗 ecsRouteTableAssociation<br/>Subnet Association"]:::awsNetwork
        end
    end

    subgraph "🌍 External"
        INTERNET["🌐 Internet<br/>0.0.0.0/0<br/>Public Traffic"]:::internet
    end

    %% VPC relationships
    VPC --> SUBNET
    VPC --> IGW
    VPC --> RT
    VPC --> SG

    %% Subnet relationships
    SUBNET --> RTA
    SUBNET --> SG

    %% Routing relationships
    RT --> RTA
    RT --> IGW
    IGW --> INTERNET
    %% Traffic flow
    SUBNET -.-> IGW
    IGW -.-> INTERNET
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