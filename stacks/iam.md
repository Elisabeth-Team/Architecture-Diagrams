# IAM Stack Architecture

## Overview
The IAM stack provides essential Identity and Access Management resources for the production ECS infrastructure. It creates service roles and policies required for ECS cluster operations, container instances, and frontend services.

## Resources
Key resources deployed by this stack:
- **ecsClusterRole**: IAM role for ECS cluster management
- **ecsInstanceRole**: IAM role for ECS container instances  
- **frontendServiceRole**: IAM role for ECS frontend service tasks
- **ecsClusterRolePolicy**: Policy for ECS cluster operations
- **ecsInstanceRolePolicy**: Policy for ECS instance operations
- **frontendServiceRolePolicy**: Policy for frontend service operations

## Dependencies
- **Stack References**: None (foundational stack)
- **External Dependencies**: AWS IAM service, ECS service principals

## Architecture Diagram

```mermaid
graph TB
    %% Define styles
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef iam fill:#FF6B6B,stroke:#C92A2A,stroke-width:2px,color:#fff
    classDef policy fill:#4ECDC4,stroke:#0CA678,stroke-width:2px,color:#fff
    classDef service fill:#45B7D1,stroke:#1976D2,stroke-width:2px,color:#fff
    
    subgraph "Stack: iam"
        subgraph "ECS Cluster Management"
            ECR[ecsClusterRole]:::iam
            ECRP[ecsClusterRolePolicy]:::policy
        end
        
        subgraph "ECS Instance Management"
            EIR[ecsInstanceRole]:::iam
            EIRP[ecsInstanceRolePolicy]:::policy
        end
        
        subgraph "Frontend Service"
            FSR[frontendServiceRole]:::iam
            FSRP[frontendServiceRolePolicy]:::policy
        end
        
        subgraph "AWS Provider"
            AWSP[AWS Provider us-east-1]:::aws
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
    
    %% Role-Policy relationships
    ECR --> ECRP
    EIR --> EIRP
    FSR --> FSRP
    
    %% Service principal relationships
    ECS --> ECR
    EC2 --> EIR
    ECS --> FSR
    
    %% Policy permissions
    ECRP --> ECS
    ECRP --> EC2
    ECRP --> ELB
    
    EIRP --> ECS
    EIRP --> LOGS
    EIRP --> ECR_SVC
    EIRP --> EC2
    
    FSRP --> LOGS
    FSRP --> ECR_SVC
    FSRP --> S3
```

## Configuration
Key configuration values used by this stack:
- **AWS Region**: us-east-1
- **AWS Provider Version**: 7.6.0

## Outputs
Key outputs that other stacks might reference:
- **ecsClusterRole.arn**: ARN of the ECS cluster role
- **ecsInstanceRole.arn**: ARN of the ECS instance role  
- **frontendServiceRole.arn**: ARN of the frontend service role

## IAM Policies Summary

### ECS Cluster Role Policy
- EC2 describe operations
- Elastic Load Balancing operations
- ECS cluster and service management

### ECS Instance Role Policy  
- ECS cluster operations
- CloudWatch Logs operations
- ECR image operations
- EC2 security group management

### Frontend Service Role Policy
- CloudWatch Logs operations
- ECR image operations  
- S3 object operations

## Notes
This is a foundational stack that provides IAM roles and policies required by other ECS-related stacks. The roles follow the principle of least privilege and are scoped to specific ECS operations.