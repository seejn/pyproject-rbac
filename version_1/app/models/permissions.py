from sqlalchemy import Column, UUID, Integer, Float, String, Text, Boolean, DateTime, Date, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
from .policies import Policy
from .roles import Role
import uuid

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    role_id = Column(UUID, ForeignKey(Role.id), nullable=False, index=True)
    policy_id = Column(UUID, ForeignKey(Policy.id), nullable=False, index=True)
    deleted = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('role_id', 'policy_id', name='_role_policy_unq'),
    )

    role = relationship("Role", back_populates="permissions")
    policy = relationship("Policy", back_populates="permissions")