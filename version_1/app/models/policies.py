from sqlalchemy import UniqueConstraint, Column, Integer, String, Float, Boolean, DateTime, Text, Enum, ForeignKey, Date, UUID
from sqlalchemy.sql import func, expression
from sqlalchemy.orm import relationship
from app.db.base import Base

import uuid

class Policy(Base):
    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    # Guest Information
    policy_name = Column(String(100), nullable=False, unique=True)
    category = Column(String(100))
    action = Column(String(20))
    deleted = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint('category', 'action', name='_category_action_unq'),)

    permissions = relationship(
        "Permission",
        back_populates="policy",
        cascade="all, delete-orphan"
    )

    roles = relationship(
        "Role",
        secondary="permissions",
        viewonly=True
    )