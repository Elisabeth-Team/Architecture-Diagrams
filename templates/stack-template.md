# {Stack Name} Architecture

## Overview
Brief description of what this stack provides and its purpose in the overall architecture.

## Resources
List of key resources deployed by this stack:
- Resource 1: Description
- Resource 2: Description

## Dependencies
- **Stack References**: List any stacks this depends on
- **External Dependencies**: APIs, services, or resources outside Pulumi management

## Architecture Diagram

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
    
    %% Example structure - replace with actual resources
    subgraph "Stack: {stack-name}"
        A[Resource A]:::aws
        B[Resource B]:::aws
        C[Database]:::db
    end
    
    subgraph "External Dependencies"
        D[External Service]
        E[Another Stack]
    end
    
    A --> B
    B --> C
    A --> D
    E --> A
```

## Configuration
Key configuration values and secrets used by this stack:
- Config 1: Description
- Secret 1: Description

## Outputs
Key outputs that other stacks might reference:
- Output 1: Description
- Output 2: Description

## Notes
Any additional notes about the architecture, deployment considerations, or known limitations.