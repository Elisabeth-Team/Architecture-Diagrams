# IAM Infrastructure Stack - Production

This diagram shows the IAM roles and policies deployed in the `iam-infrastructure` prod stack.

```mermaid
graph TB
    subgraph "AWS IAM"
        subgraph "ECS Instance Role"
            EIR[IAM Role<br/>ecsInstanceRole-ee19158]
            EIRP[Role Policy<br/>ecsInstanceRolePolicy-3efbbc2]
        end
        
        subgraph "ECS Cluster Role"
            ECR[IAM Role<br/>ecsClusterRole-85384ad]
            ECRP[Role Policy<br/>ecsClusterRolePolicy-e15a697]
        end
        
        subgraph "Frontend Service Role"
            FSR[IAM Role<br/>frontendServiceRole-ba67bd1]
            FSRP[Role Policy<br/>frontendServiceRolePolicy-f16a409]
        end
    end
    
    subgraph "AWS Services"
        EC2[EC2 Service]
        ECS[ECS Service]
        LOGS[CloudWatch Logs]
        ECR_SVC[ECR Service]
        S3[S3 Service]
    end
    
    %% Trust Relationships
    EC2 ---|AssumeRole| EIR
    ECS ---|AssumeRole| ECR
    ECS ---|AssumeRole| FSR
    
    %% Policy Attachments
    EIR ---|Has Policy| EIRP
    ECR ---|Has Policy| ECRP
    FSR ---|Has Policy| FSRP
    
    %% Permissions (ECS Instance Role)
    EIRP -.->|CreateCluster, RegisterInstance| ECS
    EIRP -.->|CreateLogStream, PutLogEvents| LOGS
    EIRP -.->|GetAuthorizationToken, BatchGetImage| ECR_SVC
    EIRP -.->|AuthorizeSecurityGroupIngress| EC2
    
    %% Permissions (ECS Cluster Role)
    ECRP -.->|Describe*, List*| EC2
    ECRP -.->|ELB Operations| ELB[Load Balancer]
    ECRP -.->|ECS Operations| ECS
    
    %% Permissions (Frontend Service Role)
    FSRP -.->|CreateLogStream, PutLogEvents| LOGS
    FSRP -.->|ECR Operations| ECR_SVC
    FSRP -.->|GetObject, PutObject| S3
    
    %% Stack Outputs (exported to other stacks)
    EIR -.->|ecsInstanceRoleArn| OUTPUTS[Stack Outputs]
    ECR -.->|ecsClusterRoleArn| OUTPUTS
    FSR -.->|frontendServiceRoleArn| OUTPUTS
    
    %% Styling
    classDef role fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef policy fill:#3F48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef service fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef outputs fill:#146EB4,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class EIR,ECR,FSR role
    class EIRP,ECRP,FSRP policy
    class EC2,ECS,LOGS,ECR_SVC,S3,ELB service
    class OUTPUTS outputs
```

## Resources Summary

### IAM Roles
- **ECS Instance Role**: `ecsInstanceRole-ee19158`
  - Trust: EC2 service
  - Purpose: EC2 instances running ECS agent
  
- **ECS Cluster Role**: `ecsClusterRole-85384ad`
  - Trust: ECS service
  - Purpose: ECS cluster management operations
  
- **Frontend Service Role**: `frontendServiceRole-ba67bd1`
  - Trust: ECS service
  - Purpose: Frontend task execution and logging

### IAM Policies

#### ECS Instance Role Policy
- **ECS Operations**: CreateCluster, DeregisterContainerInstance, DiscoverPollEndpoint, Poll, RegisterContainerInstance, StartTelemetrySession, Submit*
- **Logging**: CreateLogStream, PutLogEvents
- **ECR Access**: GetAuthorizationToken, BatchCheckLayerAvailability, GetDownloadUrlForLayer, BatchGetImage
- **EC2 Operations**: AuthorizeSecurityGroupIngress

#### ECS Cluster Role Policy
- **EC2 Operations**: Describe*
- **ELB Operations**: Describe*, RegisterTargets, DeregisterTargets, DescribeTargetHealth, DescribeListeners
- **ECS Operations**: ListClusters, ListServices, ListTasks, Describe*

#### Frontend Service Role Policy
- **Logging**: CreateLogStream, PutLogEvents
- **ECR Access**: GetDownloadUrlForLayer, BatchCheckLayerAvailability, GetAuthorizationToken, BatchGetImage
- **S3 Access**: GetObject, PutObject

### Stack Exports
This stack exports the following role ARNs for use by other stacks:
- `ecsInstanceRoleArn`: For EC2 instances
- `ecsClusterRoleArn`: For ECS cluster operations
- `frontendServiceRoleArn`: For frontend task execution

## Dependencies
- **Consumed by**: `cluster-infrastructure` stack (for ECS services and tasks)