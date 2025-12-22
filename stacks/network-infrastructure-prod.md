# Network Infrastructure Stack - Production

This diagram shows the network infrastructure resources deployed in the `network-infrastructure` prod stack.

```mermaid
graph TB
    INTERNET((Internet<br/>0.0.0.0/0))

    subgraph "AWS Region: us-east-1"
        subgraph "VPC: ecsVpc (10.0.0.0/16)"
            VPC[VPC<br/>ecsVpc<br/>CIDR: 10.0.0.0/16<br/>DNS Support: Enabled<br/>DNS Hostnames: Enabled]

            IGW[Internet Gateway<br/>ecsInternetGateway<br/>Attached to VPC]

            RT[Route Table<br/>ecsRouteTable<br/>Route: 0.0.0.0/0 → IGW]

            subgraph "Public Subnet"
                SUBNET[Subnet<br/>ecsPublicSubnet<br/>CIDR: 10.0.1.0/24<br/>Auto-assign Public IP: Yes]
            end

            SG[Security Group<br/>ecsSecurityGroup<br/>Allow HTTP & SSH]
        end
    end

    %% Internet Gateway Connection
    INTERNET ---|Public Internet Access| IGW
    IGW ---|Attached to| VPC

    %% VPC Contains Resources
    VPC ---|Contains| SUBNET
    VPC ---|Contains| RT
    VPC ---|Contains| SG

    %% Route Table Association
    RT ---|Routes 0.0.0.0/0 to| IGW
    SUBNET ---|Associated with| RT

    %% Security Group Rules
    SG -.->|Ingress: TCP 80<br/>HTTP from 0.0.0.0/0| INTERNET
    SG -.->|Ingress: TCP 22<br/>SSH from 0.0.0.0/0| INTERNET
    SG -.->|Egress: All Protocols<br/>All Ports to 0.0.0.0/0| INTERNET

    %% Stack Outputs (exported to other stacks)
    VPC -.->|vpcId| OUTPUTS[Stack Outputs<br/>Network Resource IDs]
    SUBNET -.->|publicSubnetId| OUTPUTS
    SG -.->|securityGroupId| OUTPUTS

    %% Styling
    classDef vpc fill:#3F48CC,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef subnet fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef gateway fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef security fill:#DD344C,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef routing fill:#8C4FFF,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef outputs fill:#146EB4,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef external fill:#879196,stroke:#232F3E,stroke-width:2px,color:#fff

    class VPC vpc
    class SUBNET subnet
    class IGW gateway
    class SG security
    class RT routing
    class OUTPUTS outputs
    class INTERNET external
```

## Resources Summary

### Core Network Components

- **VPC**: `ecsVpc` (10.0.0.0/16)
  - DNS Support: Enabled
  - DNS Hostnames: Enabled
  - Tag: `Name=ecs-vpc`
- **Public Subnet**: `ecsPublicSubnet` (10.0.1.0/24)
  - Auto-assign Public IP: Enabled
  - Tag: `Name=ecs-public-subnet`
- **Internet Gateway**: `ecsInternetGateway`
  - Attached to VPC
  - Tag: `Name=ecs-igw`
- **Route Table**: `ecsRouteTable`
  - Default route: 0.0.0.0/0 → Internet Gateway
  - Tag: `Name=ecs-route-table`
- **Security Group**: `ecsSecurityGroup`
  - Description: "Allow HTTP and SSH traffic"
  - Tag: `Name=ecs-security-group`

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
