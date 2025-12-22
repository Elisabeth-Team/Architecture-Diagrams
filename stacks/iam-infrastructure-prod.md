# IAM Infrastructure Stack - Production

This diagram shows the IAM roles and policies deployed in the `iam-infrastructure` prod stack.

```mermaid
graph TB
    subgraph "AWS IAM - Identity & Access Management"
        subgraph "ECS Instance Role"
            EIR[IAM Role<br/>ecsInstanceRole<br/>Principal: ec2.amazonaws.com]
            EIRP[Inline Policy<br/>ecsInstanceRolePolicy]
        end
        
        subgraph "ECS Cluster Role"
            ECR[IAM Role<br/>ecsClusterRole<br/>Principal: ecs.amazonaws.com]
            ECRP[Inline Policy<br/>ecsClusterRolePolicy]
        end
        
        subgraph "Frontend Service Role"
            FSR[IAM Role<br/>frontendServiceRole<br/>Principal: ecs-tasks.amazonaws.com]
            FSRP[Inline Policy<br/>frontendServiceRolePolicy]
        end
    end
    
    subgraph "AWS Services - Trust & Permissions"
        EC2[EC2 Service<br/>Trusted by Instance Role]
        ECS_SVC[ECS Service<br/>Trusted by Cluster Role]
        ECS_TASKS[ECS Tasks Service<br/>Trusted by Service Role]
        LOGS[CloudWatch Logs<br/>Log Stream Management]
        ECR_SVC[ECR Service<br/>Container Image Registry]
        S3[S3 Service<br/>Object Storage]
        ELB[Elastic Load Balancing<br/>Target Management]
    end
    
    %% Trust Relationships (AssumeRole)
    EC2 ---|Trusts & Assumes| EIR
    ECS_SVC ---|Trusts & Assumes| ECR
    ECS_TASKS ---|Trusts & Assumes| FSR
    
    %% Policy Attachments
    EIR ---|Inline Policy| EIRP
    ECR ---|Inline Policy| ECRP
    FSR ---|Inline Policy| FSRP
    
    %% Permissions (ECS Instance Role)
    EIRP -.->|CreateCluster, DeregisterContainerInstance<br/>DiscoverPollEndpoint, Poll<br/>RegisterContainerInstance<br/>StartTelemetrySession, Submit*| ECS_SVC
    EIRP -.->|CreateLogStream<br/>PutLogEvents| LOGS
    EIRP -.->|GetAuthorizationToken<br/>BatchCheckLayerAvailability<br/>GetDownloadUrlForLayer<br/>BatchGetImage| ECR_SVC
    EIRP -.->|AuthorizeSecurityGroupIngress| EC2
    
    %% Permissions (ECS Cluster Role)
    ECRP -.->|Describe*| EC2
    ECRP -.->|Describe*, RegisterTargets<br/>DeregisterTargets<br/>DescribeTargetHealth<br/>DescribeListeners| ELB
    ECRP -.->|ListClusters, ListServices<br/>ListTasks, Describe*| ECS_SVC
    
    %% Permissions (Frontend Service Role)
    FSRP -.->|CreateLogStream<br/>PutLogEvents| LOGS
    FSRP -.->|GetDownloadUrlForLayer<br/>BatchCheckLayerAvailability<br/>GetAuthorizationToken<br/>BatchGetImage| ECR_SVC
    FSRP -.->|GetObject<br/>PutObject| S3
    
    %% Stack Outputs (exported to other stacks)
    EIR -.->|ecsInstanceRoleArn| OUTPUTS[Stack Outputs<br/>Exported ARNs]
    ECR -.->|ecsClusterRoleArn| OUTPUTS
    FSR -.->|frontendServiceRoleArn| OUTPUTS
    
    %% Styling
    classDef role fill:#DD344C,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef policy fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef service fill:#8C4FFF,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef outputs fill:#146EB4,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class EIR,ECR,FSR role
    class EIRP,ECRP,FSRP policy
    class EC2,ECS_SVC,ECS_TASKS,LOGS,ECR_SVC,S3,ELB service
    class OUTPUTS outputs
```

## Resources Summary

### IAM Roles
- **ECS Instance Role**: `ecsInstanceRole`
  - Trust: EC2 service (`ec2.amazonaws.com`)
  - Purpose: EC2 instances running ECS agent (for EC2 launch type)
  
- **ECS Cluster Role**: `ecsClusterRole`
  - Trust: ECS service (`ecs.amazonaws.com`)
  - Purpose: ECS cluster management operations
  
- **Frontend Service Role**: `frontendServiceRole`
  - Trust: ECS Tasks service (`ecs-tasks.amazonaws.com`)
  - Purpose: Task execution role for pulling images, logging, and application permissions

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