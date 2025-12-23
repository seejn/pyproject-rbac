"""Permission data preparer."""

from typing import List, Dict, Any

from sqlalchemy.orm import Session

from app.models import Policy, Role, Permission
from seeds.preparers.base import BasePreparer
from seeds.utils.logger import get_logger

logger = get_logger(__name__)


class PermissionPreparer(BasePreparer):
    """Preparer for Permission model."""

    @property
    def table_name(self) -> str:
        return "permissions"
    
    def prepare(self, db: Session, data: List[Dict[str, Any]]) -> List[Permission]:
        """
        Prepare Permission objects from raw data with role and policy lookups.

        Args:
            db: Database session for lookups
            data: List of Permission dictionaries

        Returns:
            List of Permission instances
        """
        permissions_data = []

        for item in data:
            role_name = item.get("role")
            policy_names = item.get("policies")

            role = db.query(Role).filter(Role.role == role_name).first()
            if not role:
                logger.warning(f"Role '{role_name}' not found, skipping permissions")
                continue

            if policy_names == "*":
                policies = db.query(Policy).all()
            else:
                policies = db.query(Policy).filter(
                    Policy.policy_name.in_(policy_names)
                ).all()
            
            if not policies:
                logger.warning(f"No policies found for role '{role_name}'")
                continue

            permissions_data.extend([
                Permission(role_id=role.id, policy_id=policy.id)
                for policy in policies
            ])

        return permissions_data