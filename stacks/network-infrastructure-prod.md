# Network Infrastructure Stack - Production

This diagram shows the network infrastructure resources deployed in the `network-infrastructure` prod stack.

```mermaid
graph TB
    subgraph "AWS Region: us-east-1"
        subgraph "VPC: ecs-vpc (10.0.0.0/16)"
            VPC[VPC<br/>vpc-05d6664f26f91261b<br/>10.0.0.0/16<br/>DNS: Enabled]

            subgraph "Availability Zone: us-east-1a"
                SUBNET[Public Subnet<br/>subnet-05b39df7a84c55aff<br/>10.0.1.0/24<br/>Auto-assign Public IP]
            end

            IGW[Internet Gateway<br/>igw-0376448381106889d<br/>ecs-igw]
            RT[Route Table<br/>rtb-0542e80ea0ff882ec<br/>ecs-route-table]
            SG[Security Group<br/>sg-0d52a1c384768365e<br/>ecsSecurityGroup-ac26379]
        end
    end

    INTERNET((Internet))

    %% Connections
    INTERNET ---|Public Access| IGW
    IGW ---|Attached to| VPC
    VPC ---|Contains| SUBNET
    RT ---|Route: 0.0.0.0/0 →| IGW
    SUBNET ---|Associated with| RT
    SG ---|Protects resources in| VPC

    %% Security Group Rules
    SG -.->|Ingress: TCP 80 from 0.0.0.0/0| INTERNET
    SG -.->|Ingress: TCP 22 from 0.0.0.0/0| INTERNET
    SG -.->|Egress: All traffic to 0.0.0.0/0| INTERNET

    %% Stack Outputs (exported to other stacks)
    SUBNET -.->|publicSubnetId| OUTPUTS[Stack Outputs]
    VPC -.->|vpcId| OUTPUTS
    SG -.->|securityGroupId| OUTPUTS

    %% Styling
    classDef vpc fill:#3F48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef subnet fill:#146EB4,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef gateway fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef security fill:#DD344C,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef routing fill:#8C4FFF,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef outputs fill:#FF6600,stroke:#232F3E,stroke-width:2px,color:#fff
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

- **VPC**: `vpc-05d6664f26f91261b` (ecs-vpc)
  - CIDR Block: `10.0.0.0/16`
  - DNS Support: Enabled
  - DNS Hostnames: Enabled
  - Instance Tenancy: Default
  - ARN: `arn:aws:ec2:us-east-1:052848974346:vpc/vpc-05d6664f26f91261b`

- **Public Subnet**: `subnet-05b39df7a84c55aff` (ecs-public-subnet)
  - CIDR Block: `10.0.1.0/24`
  - Availability Zone: `us-east-1a` (AZ ID: use1-az1)
  - Auto-assign Public IP: Enabled
  - ARN: `arn:aws:ec2:us-east-1:052848974346:subnet/subnet-05b39df7a84c55aff`

- **Internet Gateway**: `igw-0376448381106889d` (ecs-igw)
  - Attached to VPC: `vpc-05d6664f26f91261b`
  - ARN: `arn:aws:ec2:us-east-1:052848974346:internet-gateway/igw-0376448381106889d`

- **Route Table**: `rtb-0542e80ea0ff882ec` (ecs-route-table)
  - Routes:
    - `0.0.0.0/0` → `igw-0376448381106889d` (Internet Gateway)
  - Associated with: `subnet-05b39df7a84c55aff`
  - ARN: `arn:aws:ec2:us-east-1:052848974346:route-table/rtb-0542e80ea0ff882ec`

- **Security Group**: `sg-0d52a1c384768365e` (ecsSecurityGroup-ac26379)
  - Description: Allow HTTP and SSH traffic
  - VPC: `vpc-05d6664f26f91261b`
  - ARN: `arn:aws:ec2:us-east-1:052848974346:security-group/sg-0d52a1c384768365e`

### Security Configuration

#### Ingress Rules
- **HTTP**: TCP port 80 from `0.0.0.0/0` (anywhere)
- **SSH**: TCP port 22 from `0.0.0.0/0` (anywhere)

#### Egress Rules
- **All Traffic**: All protocols, all ports to `0.0.0.0/0` (anywhere)

### Stack Exports

This stack exports the following outputs for use by other stacks:

- `vpcId`: `vpc-05d6664f26f91261b`
- `publicSubnetId`: `subnet-05b39df7a84c55aff`
- `securityGroupId`: `sg-0d52a1c384768365e`

## Stack Information

- **Project**: `network-infrastructure`
- **Stack**: `networkstack`
- **Organization**: `elisabeth-demo`
- **Environment**: `prod`
- **Repository**: `github.com/lichtie/prod-infrastructure`
- **Path**: `network/`
- **Provider**: AWS (pulumi-aws v6.13.3)
- **Region**: us-east-1

## Dependencies

- **Consumed by**: Stacks requiring VPC and networking resources for ECS or other compute deployments
- **Note**: While originally created for the cluster-infrastructure stack, these network resources remain available for future deployments
