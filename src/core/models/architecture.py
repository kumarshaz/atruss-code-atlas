import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from src.core.database import Base


class ArchitectureComponent(Base):
    __tablename__ = "architecture_components"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("git_repositories.id"), nullable=False, index=True)
    component_name = Column(String, nullable=False)
    component_type = Column(String, nullable=False) # API_ROUTE, DATA_ACCESS_LAYER
    file_source = Column(String, nullable=False)
