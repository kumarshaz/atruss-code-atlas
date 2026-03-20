import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.core.database import Base


class GitRepository(Base):
    __tablename__ = "git_repositories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider = Column(String, nullable=False, default="github")
    namespace = Column(String, nullable=False, index=True) # e.g., org/repo
    primary_ecosystem = Column(String, nullable=True)     # e.g., python
    framework = Column(String, nullable=True)             # e.g., fastapi
    clone_url = Column(String, nullable=False)
    is_monorepo = Column(Boolean, default=False)
