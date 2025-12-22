from sqlalchemy import Column, UUID, Integer, Float, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.sql import func, expression
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    role = Column(String(50), unique=True, nullable=False)
    deleted = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    permissions = relationship(
        "Permission",
        back_populates="role",
        cascade="all, delete-orphan"
    )

    # Relationship to access policies directly
    policies = relationship(
        "Policy",
        secondary="permissions",
        viewonly=True
    )