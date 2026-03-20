import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from src.core.database import Base


class CoverageMetric(Base):
    __tablename__ = "coverage_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("git_repositories.id"), nullable=False, index=True)
    runner_type = Column(String, nullable=False)
    total_coverage_percent = Column(Float, nullable=False)
    report_file_source = Column(String, nullable=False)
