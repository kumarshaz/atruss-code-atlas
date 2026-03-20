import enum
import uuid

from sqlalchemy import JSON, Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from src.core.database import Base


class DependencyType(str, enum.Enum):
    SEQUENTIAL = "SEQUENTIAL"

class FindingSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class PipelineWorkflow(Base):
    __tablename__ = "pipeline_workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("git_repositories.id"), nullable=False, index=True)
    file_path = Column(String, nullable=False)
    trigger_events = Column(JSON, nullable=True)
    coverage_metric_id = Column(UUID(as_uuid=True), ForeignKey("coverage_metrics.id"), nullable=True)

class PipelineJob(Base):
    __tablename__ = "pipeline_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("pipeline_workflows.id"), nullable=False)
    job_name = Column(String, nullable=False)
    runner = Column(String, nullable=True)
    status_history = Column(JSON, nullable=True)

class JobDependency(Base):
    __tablename__ = "job_dependencies"

    source_job_id = Column(UUID(as_uuid=True), ForeignKey("pipeline_jobs.id"), primary_key=True)
    target_job_id = Column(UUID(as_uuid=True), ForeignKey("pipeline_jobs.id"), primary_key=True)
    dependency_type = Column(Enum(DependencyType), default=DependencyType.SEQUENTIAL)

class AntiPatternFinding(Base):
    __tablename__ = "anti_pattern_findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String, nullable=False)  # "WORKFLOW" or "ARCHITECTURE"
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    severity = Column(Enum(FindingSeverity), nullable=False)
    description = Column(String, nullable=False)
