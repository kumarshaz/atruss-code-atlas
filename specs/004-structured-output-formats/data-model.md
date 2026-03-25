# Data Models: GitHub Orchestration Parity

## Core Concept
The system bridges exactly 4 core entities mirroring the physical topology. Data is exported deterministically via 8 phases into timestamped `exports/{timestamp}` directories.

### 1. Repository Discovery Output (CSV & JSON/YAML properties)
*Dynamically maps to available GitHub payload endpoints without strictly adhering to an ADO parity translation. Columns will auto-flatten based dict keys discovered at runtime.*

### 2. Pipeline Visualization Output (CSV)
To feed analytical queries natively, the deployment chains are flattened:
- `RepoName` (string)
- `WorkflowName` (string)
- `DeploymentTarget` (string)
- `DeploymentResource` (string)

### 3. Pipeline JSON Envelope
Contains metadata wrapper for pipeline JSON dumps:
```json
{
  "count": 123,
  "items": [
    {
      "repoId": "string",
      "repoName": "string",
      "workflowId": 1245,
      "workflowName": "string",
      "environmentNames": ["array"],
      "deploymentTargetId": 123,
      "deploymentTargetType": "environment | runnerGroup",
      "deploymentTargetName": "string",
      "linkageMethod": "workflow-environment | workflow-runner-group | reusable-workflow",
      "iisConfig": null,
      "k8sContext": null,
      "resourceNames": ["array"]
    }
  ]
}
```

### 4. Mermaid Graphs
Arc42 Markdown visually compresses the YAML deployments into exactly 3 subgraphs for `Actions Workflows`, `Deployment Targets`, and `Deployment Resources`.
