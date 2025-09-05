# Production Infrastructure Overview

## Architecture Summary
High-level overview of the entire production infrastructure across all stacks.

## Stack Relationships
Description of how stacks relate to each other and share resources through StackReferences.

## Master Architecture Diagram

```mermaid
graph TB
    %% Define styles
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef gcp fill:#4285F4,stroke:#1a73e8,stroke-width:2px,color:#fff
    classDef azure fill:#0078D4,stroke:#005a9e,stroke-width:2px,color:#fff
    classDef k8s fill:#326CE5,stroke:#1e3a8a,stroke-width:2px,color:#fff
    classDef db fill:#336791,stroke:#1e3a8a,stroke-width:2px,color:#fff
    classDef lb fill:#28A745,stroke:#155724,stroke-width:2px,color:#fff
    classDef storage fill:#FFC107,stroke:#856404,stroke-width:2px,color:#000
    classDef stack fill:#6C757D,stroke:#495057,stroke-width:3px,color:#fff
    
    %% Example structure - replace with actual stacks and relationships
    subgraph "Production Environment"
        subgraph "Stack 1"
            S1A[Key Resource A]:::aws
            S1B[Key Resource B]:::aws
        end
        
        subgraph "Stack 2"
            S2A[Key Resource C]:::gcp
            S2B[Key Resource D]:::db
        end
        
        subgraph "Stack 3"
            S3A[Key Resource E]:::k8s
            S3B[Key Resource F]:::lb
        end
    end
    
    subgraph "External Services"
        EXT1[External API]
        EXT2[Third-party Service]
    end
    
    %% Stack relationships via StackReferences
    S1A --> S2A
    S2B --> S3A
    S1B --> S3B
    
    %% External connections
    S1A --> EXT1
    S3A --> EXT2
```

## Data Flow
Description of how data flows between stacks and external systems.

## Security Boundaries
Overview of security zones, network boundaries, and access controls.

## Disaster Recovery
High-level disaster recovery strategy and cross-stack dependencies.

## Monitoring & Observability
Overview of monitoring, logging, and alerting across all stacks.