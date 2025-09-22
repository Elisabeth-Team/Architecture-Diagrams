# Cluster Infrastructure Stack - Production

This diagram shows the ECS cluster and containerized applications deployed in the `cluster-infrastructure` prod stack.

```mermaid
graph TB
    subgraph "External Dependencies"
        IAM_STACK[IAM Infrastructure Stack]
        NET_STACK[Network Infrastructure Stack]
    end
    
    subgraph "AWS ECS - us-east-1"
        subgraph "ECS Cluster: my-ecs-cluster"
            CLUSTER[ECS Cluster<br/>my-ecs-cluster]
            
            subgraph "Frontend Service"
                SERVICE[ECS Service<br/>frontendService-7ab8c00<br/>Desired: 1 task]
                TASK_DEF[Task Definition<br/>frontend-task:2<br/>CPU: 256, Memory: 512MB]
                
                subgraph "Container"
                    CONTAINER[Container<br/>frontend-container<br/>nginx:latest<br/>Port: 80]
                end
            end
        end
        
        subgraph "CloudWatch Logs"
            LOG_GROUP[Log Group<br/>/ecs/frontend-task<br/>Retention: 14 days]
        end
    end
    
    subgraph "Network (from network-infrastructure)"
        VPC_REF[VPC<br/>vpc-0c14c65de928961e3]
        SUBNET_REF[Public Subnet<br/>subnet-01d1c207006d52e59]
        SG_REF[Security Group<br/>sg-011d6da5dcd69ec9f]
    end
    
    subgraph "IAM (from iam-infrastructure)"
        EXEC_ROLE[Execution Role<br/>frontendServiceRole-ba67bd1]
        TASK_ROLE[Task Role<br/>frontendServiceRole-ba67bd1]
    end
    
    INTERNET((Internet))
    
    %% Stack References
    NET_STACK -.->|Provides VPC, Subnet, SG| VPC_REF
    NET_STACK -.->|Provides VPC, Subnet, SG| SUBNET_REF
    NET_STACK -.->|Provides VPC, Subnet, SG| SG_REF
    IAM_STACK -.->|Provides Roles| EXEC_ROLE
    IAM_STACK -.->|Provides Roles| TASK_ROLE
    
    %% ECS Relationships
    CLUSTER ---|Contains| SERVICE
    SERVICE ---|Uses| TASK_DEF
    TASK_DEF ---|Defines| CONTAINER
    SERVICE ---|Runs in| SUBNET_REF
    SERVICE ---|Protected by| SG_REF
    
    %% IAM Relationships
    TASK_DEF ---|Execution Role| EXEC_ROLE
    TASK_DEF ---|Task Role| TASK_ROLE
    
    %% Logging
    CONTAINER ---|Logs to| LOG_GROUP
    
    %% Network Flow
    INTERNET ---|HTTP:80| SG_REF
    SG_REF ---|Allows traffic to| CONTAINER
    CONTAINER ---|Deployed in| SUBNET_REF
    SUBNET_REF ---|Part of| VPC_REF
    
    %% Launch Configuration
    SERVICE -.->|Launch Type: FARGATE| AWS_FARGATE[AWS Fargate]
    SERVICE -.->|Public IP: Enabled| SUBNET_REF
    
    %% Styling
    classDef cluster fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef service fill:#3F48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef container fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef logs fill:#8C4FFF,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef network fill:#146EB4,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef iam fill:#DD344C,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef stack fill:#879196,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef fargate fill:#FF6600,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class CLUSTER cluster
    class SERVICE,TASK_DEF service
    class CONTAINER container
    class LOG_GROUP logs
    class VPC_REF,SUBNET_REF,SG_REF network
    class EXEC_ROLE,TASK_ROLE iam
    class IAM_STACK,NET_STACK stack
    class AWS_FARGATE fargate
```

## Resources Summary

### ECS Resources
- **Cluster**: `my-ecs-cluster`
- **Service**: `frontendService-7ab8c00`
  - Desired Count: 1 task
  - Launch Type: AWS Fargate
  - Platform Version: LATEST
- **Task Definition**: `frontend-task:2`
  - CPU: 256 units
  - Memory: 512 MB
  - Network Mode: awsvpc
  - Requires Compatibility: FARGATE

### Container Configuration
- **Container Name**: `frontend-container`
- **Image**: `nginx:latest`
- **Port Mapping**: Container port 80 → Host port 80
- **Protocol**: TCP
- **Essential**: Yes

### Logging Configuration
- **Log Group**: `/ecs/frontend-task`
- **Log Driver**: awslogs
- **Region**: us-east-1
- **Stream Prefix**: ecs
- **Retention**: 14 days

### Network Configuration
- **VPC**: Inherited from network-infrastructure stack
- **Subnet**: Public subnet with auto-assign public IP enabled
- **Security Group**: Allows HTTP (80) and SSH (22) from internet

### IAM Configuration
- **Execution Role**: `frontendServiceRole-ba67bd1` (for pulling images, logging)
- **Task Role**: `frontendServiceRole-ba67bd1` (for application permissions)

## Stack Dependencies

### Consumes from network-infrastructure
- `vpcId`: VPC identifier for network placement
- `publicSubnetId`: Subnet for task deployment
- `securityGroupId`: Security group for network access control

### Consumes from iam-infrastructure
- `frontendServiceRoleArn`: IAM role for task execution and application permissions
- `ecsClusterRoleArn`: IAM role for cluster operations
- `ecsInstanceRoleArn`: IAM role for EC2 instances (if using EC2 launch type)

## Data Flow
1. **Internet Traffic** → Security Group (port 80) → Frontend Container
2. **Container Logs** → CloudWatch Logs (`/ecs/frontend-task`)
3. **Image Pull** → ECR (via execution role permissions)
4. **Task Networking** → Public subnet with internet gateway access