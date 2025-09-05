# Production Infrastructure Overview

## Architecture Summary
Complete overview of the production infrastructure. Currently consists of the foundational IAM stack that provides identity and access management for ECS-based workloads.

## Stack Summary
- **iam**: 7 IAM resources (3 roles, 3 policies, 1 provider)

## Master Architecture Diagram

```mermaid
graph TB
    %% Define styles
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef iam fill:#FF6B6B,stroke:#C92A2A,stroke-width:2px,color:#fff
    classDef policy fill:#4ECDC4,stroke:#0CA678,stroke-width:2px,color:#fff
    classDef service fill:#45B7D1,stroke:#1976D2,stroke-width:2px,color:#fff
    classDef stack fill:#6C757D,stroke:#495057,stroke-width:3px,color:#fff
    
    subgraph "Production Environment - us-east-1"
        subgraph "IAM Stack"
            subgraph "ECS Roles & Policies"
                ECR[ECS Cluster Role]:::iam
                EIR[ECS Instance Role]:::iam
                FSR[Frontend Service Role]:::iam
                
                ECRP[Cluster Policy]:::policy
                EIRP[Instance Policy]:::policy
                FSRP[Service Policy]:::policy
            end
        end
        
        subgraph "Future Stacks"
            FUTURE1[ECS Infrastructure Stack]:::stack
            FUTURE2[Application Stack]:::stack
            FUTURE3[Networking Stack]:::stack
        end
    end
    
    subgraph "AWS Services"
        ECS[ECS Service]:::service
        EC2[EC2 Service]:::service
        ECR_SVC[ECR Service]:::service
        LOGS[CloudWatch Logs]:::service
        S3[S3 Service]:::service
        ELB[Elastic Load Balancing]:::service
    end
    
    %% Current relationships
    ECR --> ECRP
    EIR --> EIRP
    FSR --> FSRP
    
    %% Service relationships
    ECRP --> ECS
    ECRP --> EC2
    ECRP --> ELB
    
    EIRP --> ECS
    EIRP --> LOGS
    EIRP --> ECR_SVC
    
    FSRP --> LOGS
    FSRP --> ECR_SVC
    FSRP --> S3
    
    %% Future stack dependencies (will be updated when stacks are created)
    ECR -.-> FUTURE1
    EIR -.-> FUTURE1
    FSR -.-> FUTURE2
    FUTURE3 -.-> FUTURE1
```

## Data Flow
The IAM stack provides the foundational security layer for ECS-based applications:

1. **ECS Cluster Role**: Manages cluster-level operations and load balancer integration
2. **ECS Instance Role**: Handles container instance registration and image pulling
3. **Frontend Service Role**: Manages application-level permissions for logging and storage

## Security Boundaries
- **IAM Boundary**: All roles follow principle of least privilege
- **Service Isolation**: Each role is scoped to specific ECS components
- **Regional Scope**: All resources deployed in us-east-1

## Stack Relationships
Currently a single foundational stack. Future stacks will reference these IAM roles:

- **ECS Infrastructure Stack**: Will use ecsClusterRole and ecsInstanceRole
- **Application Stack**: Will use frontendServiceRole
- **Networking Stack**: May create additional security group rules referenced by instance policy

## Monitoring & Observability
- CloudWatch Logs permissions configured for all ECS components
- IAM role usage can be monitored through CloudTrail
- Policy effectiveness can be tracked through Access Analyzer

## Next Steps
The infrastructure is ready for:
1. ECS cluster and service definitions
2. Application deployment configurations  
3. Networking and security group setup
4. Load balancer and target group configurations