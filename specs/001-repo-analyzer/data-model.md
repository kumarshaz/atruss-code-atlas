# Phase 1: Data Model

## GitRepository
- `id`: UUID (Primary Key)
- `provider`: String ("github", "bitbucket", "ado")
- `namespace`: String (e.g., "org-name/repo-name")
- `primary_ecosystem`: String (e.g., "python", "java-spring")
- `framework`: String (e.g., "fastapi", "react")
- `clone_url`: String
- `is_monorepo`: Boolean

## PipelineWorkflow
- `id`: UUID
- `repository_id`: UUID (Foreign Key)
- `file_path`: String (e.g., ".github/workflows/deploy.yml")
- `trigger_events`: JSON Array (e.g., ["push", "pull_request"])

## PipelineJob (Graph Node)
- `id`: UUID
- `workflow_id`: UUID
- `job_name`: String
- `runner`: String
- `status_history`: JSON

## JobDependency (Graph Edge)
- `source_job_id`: UUID
- `target_job_id`: UUID
- `dependency_type`: Enum (Sequential)

## ArchitectureComponent
- `id`: UUID
- `repository_id`: UUID
- `component_name`: String
- `component_type`: Enum ("API_ROUTE", "DATA_ACCESS_LAYER")
- `file_source`: String

## AntiPatternFinding
- `id`: UUID
- `entity_type`: Enum ("WORKFLOW", "ARCHITECTURE")
- `entity_id`: UUID
- `severity`: Enum ("CRITICAL", "HIGH", "MEDIUM", "LOW")
- `description`: String
