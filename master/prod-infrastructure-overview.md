# Production Infrastructure Overview

This master diagram shows the complete production infrastructure across all Pulumi stacks, including cross-stack dependencies and data flow.

```mermaid
graph TB
    subgraph "Internet"
        USERS[Users/Clients]
        INTERNET((Internet))
    end
    
    subgraph "AWS Account: 052848974346"
        subgraph "IAM Infrastructure Stack"
            subgraph "IAM Roles & Policies"
                ECS_INST_ROLE[ECS Instance Role<br/>ecsInstanceRole-ee19158]
                ECS_CLUSTER_ROLE[ECS Cluster Role<br/>ecsClusterRole-85384ad]
                FRONTEND_ROLE[Frontend Service Role<br/>frontendServiceRole-ba67bd1]
            end
        end
        
        subgraph "Network Infrastructure Stack"
            subgraph "VPC: ecs-vpc (10.0.0.0/16)"
                IGW[Internet Gateway<br/>igw-08fbc3e9c0a7e57fd]
                
                subgraph "AZ: us-east-1b"
                    PUBLIC_SUBNET[Public Subnet<br/>10.0.1.0/24<br/>subnet-01d1c207006d52e59]
                end
                
                ROUTE_TABLE[Route Table<br/>rtb-0f5f08fe751ed9044]
                SECURITY_GROUP[Security Group<br/>sg-011d6da5dcd69ec9f<br/>HTTP:80, SSH:22]
            end
        end
        
        subgraph "Cluster Infrastructure Stack"
            subgraph "ECS Cluster: my-ecs-cluster"
                ECS_CLUSTER[ECS Cluster<br/>my-ecs-cluster]
                
                subgraph "Frontend Service"
                    ECS_SERVICE[ECS Service<br/>frontendService-7ab8c00<br/>Desired: 1 task]
                    TASK_DEF[Task Definition<br/>frontend-task:2<br/>Fargate: 256 CPU, 512 MB]
                    
                    subgraph "Running Task"
                        NGINX_CONTAINER[Container<br/>nginx:latest<br/>Port: 80]
                    end
                end
            end
            
            subgraph "CloudWatch Logs"
                LOG_GROUP[Log Group<br/>/ecs/frontend-task<br/>14 days retention]
            end
        end
        
        subgraph "AWS Services"
            ECR[Elastic Container Registry]
            FARGATE[AWS Fargate]
            CLOUDWATCH[CloudWatch Logs]
        end
    end
    
    %% External Traffic Flow
    USERS ---|HTTP Requests| INTERNET
    INTERNET ---|Port 80| IGW
    
    %% Network Flow
    IGW ---|Attached to VPC| PUBLIC_SUBNET
    ROUTE_TABLE ---|Routes 0.0.0.0/0 to| IGW
    PUBLIC_SUBNET ---|Associated with| ROUTE_TABLE
    SECURITY_GROUP ---|Protects| PUBLIC_SUBNET
    
    %% Cross-Stack Dependencies (Stack References)
    ECS_INST_ROLE -.->|ecsInstanceRoleArn| ECS_SERVICE
    ECS_CLUSTER_ROLE -.->|ecsClusterRoleArn| ECS_SERVICE
    FRONTEND_ROLE -.->|frontendServiceRoleArn| TASK_DEF
    PUBLIC_SUBNET -.->|publicSubnetId| ECS_SERVICE
    SECURITY_GROUP -.->|securityGroupId| ECS_SERVICE
    
    %% ECS Relationships
    ECS_CLUSTER ---|Contains| ECS_SERVICE
    ECS_SERVICE ---|Runs| TASK_DEF
    TASK_DEF ---|Defines| NGINX_CONTAINER
    ECS_SERVICE ---|Deployed in| PUBLIC_SUBNET
    ECS_SERVICE ---|Protected by| SECURITY_GROUP
    
    %% Service Integrations
    TASK_DEF ---|Pulls images from| ECR
    ECS_SERVICE ---|Runs on| FARGATE
    NGINX_CONTAINER ---|Logs to| LOG_GROUP
    LOG_GROUP ---|Stored in| CLOUDWATCH
    
    %% Data Flow
    INTERNET ---|HTTP:80| SECURITY_GROUP
    SECURITY_GROUP ---|Allows traffic| NGINX_CONTAINER
    NGINX_CONTAINER ---|Serves content| SECURITY_GROUP
    SECURITY_GROUP ---|Response| INTERNET
    
    %% IAM Permissions Flow
    FRONTEND_ROLE -.->|ECR permissions| ECR
    FRONTEND_ROLE -.->|Logging permissions| CLOUDWATCH
    
    %% Stack Boundaries
    subgraph "Stack Outputs & Dependencies"
        IAM_OUTPUTS[IAM Stack Outputs:<br/>• ecsInstanceRoleArn<br/>• ecsClusterRoleArn<br/>• frontendServiceRoleArn]
        NET_OUTPUTS[Network Stack Outputs:<br/>• vpcId<br/>• publicSubnetId<br/>• securityGroupId]
        CLUSTER_INPUTS[Cluster Stack Inputs:<br/>• IAM role ARNs<br/>• Network resource IDs]
    end
    
    %% Styling
    classDef iam fill:#DD344C,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef network fill:#3F48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef cluster fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef container fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef aws fill:#8C4FFF,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef logs fill:#146EB4,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef external fill:#879196,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef outputs fill:#FF6600,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class ECS_INST_ROLE,ECS_CLUSTER_ROLE,FRONTEND_ROLE iam
    class IGW,PUBLIC_SUBNET,ROUTE_TABLE,SECURITY_GROUP network
    class ECS_CLUSTER,ECS_SERVICE,TASK_DEF cluster
    class NGINX_CONTAINER container
    class ECR,FARGATE,CLOUDWATCH aws
    class LOG_GROUP logs
    class USERS,INTERNET external
    class IAM_OUTPUTS,NET_OUTPUTS,CLUSTER_INPUTS outputs
```

## Architecture Overview

### Stack Architecture
The production infrastructure is organized into three logical Pulumi stacks:

1. **IAM Infrastructure Stack** (`iam-infrastructure`)
   - Manages all IAM roles and policies
   - Provides role ARNs to dependent stacks
   - Follows principle of least privilege

2. **Network Infrastructure Stack** (`network-infrastructure`)
   - Manages VPC, subnets, routing, and security groups
   - Provides network resource IDs to dependent stacks
   - Establishes secure network boundaries

3. **Cluster Infrastructure Stack** (`cluster-infrastructure`)
   - Manages ECS cluster, services, and task definitions
   - Consumes outputs from IAM and Network stacks
   - Runs containerized applications

### Cross-Stack Dependencies

#### IAM → Cluster
- `ecsInstanceRoleArn`: For EC2 instances (if using EC2 launch type)
- `ecsClusterRoleArn`: For ECS cluster management operations
- `frontendServiceRoleArn`: For task execution and application permissions

#### Network → Cluster
- `vpcId`: VPC identifier for resource placement
- `publicSubnetId`: Subnet for task deployment
- `securityGroupId`: Security group for access control

### Data Flow Patterns

#### User Request Flow
1. **Client Request** → Internet → Internet Gateway
2. **Network Routing** → VPC → Public Subnet
3. **Security Filtering** → Security Group (allows HTTP:80)
4. **Container Processing** → Nginx container
5. **Response Path** → Reverse of request flow

#### Container Lifecycle Flow
1. **Image Pull** → ECR (via frontend service role)
2. **Task Launch** → Fargate platform
3. **Network Assignment** → Public subnet with auto-assign IP
4. **Log Streaming** → CloudWatch Logs group

#### Security & Permissions Flow
1. **Task Execution** → Frontend service role assumes permissions
2. **ECR Access** → Role allows image pulling
3. **Logging Access** → Role allows log stream creation and writing
4. **Network Security** → Security group controls traffic

### Resource Relationships

#### High-Level Architecture
- **Compute**: AWS Fargate (serverless containers)
- **Networking**: VPC with public subnet and internet gateway
- **Security**: IAM roles with least-privilege policies + security groups
- **Monitoring**: CloudWatch Logs with 14-day retention
- **Container Registry**: ECR for image storage

#### Scaling & Availability
- **Current Configuration**: Single AZ deployment (us-east-1b)
- **Service Scaling**: ECS service with desired count of 1
- **Container Platform**: Fargate (serverless, managed scaling)

### Infrastructure Characteristics

#### Security Posture
- ✅ IAM roles with specific, limited permissions
- ✅ Security groups with defined ingress/egress rules
- ⚠️ Public subnet with internet access (consider private subnet + ALB)
- ⚠️ SSH access allowed (port 22) - review necessity

#### Operational Considerations
- **Monitoring**: CloudWatch Logs integration
- **Deployment**: Fargate platform (no server management)
- **Networking**: Single AZ (consider multi-AZ for HA)
- **Storage**: Stateless containers (no persistent volumes)

## Repository Information
All infrastructure is managed through Infrastructure as Code using Pulumi:
- **Repository**: `github.com/lichtie/prod-infrastructure`
- **Organization**: `elisabeth-demo`
- **Environment**: `prod`