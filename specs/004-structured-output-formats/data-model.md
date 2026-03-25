# Phase 1: Data Models

## Discovery Manifest

The structure represents the discovered repositories.

```python
class DiscoveryManifestItem(BaseModel):
    name: str # The repository name
    clone_url: str # The clone URI
    ecosystem: str # Detected ecosystem (e.g. Python, Node.js)
```
- **Serialization**: 
  - **CSV**: Columns -> `name`, `clone_url`, `ecosystem`. Each item is a row.
  - **JSON**: Array of objects.
  - **YAML**: Sequence of mappings.

## Pipeline DAG

The structure represents the workflow graph.

```python
class Node(BaseModel):
    node_id: str
    name: str
    ecosystem_type: str = "pipeline"

class Edge(BaseModel):
    source: str # node_id
    target: str # node_id
    relationship: str = "needs"

class PipelineDAG(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
```
- **Serialization**:
  - **CSV**: Output requires two files logically, or exporting the list of Nodes. Best approach is a Node List export, or an Edge List export if dependency mapping is requested.
  - **JSON**: Nested object `{"nodes": [...], "edges": [...]}`.
  - **YAML**: Document with `nodes:` and `edges:` sequences.
