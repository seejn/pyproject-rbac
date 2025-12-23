"""role data preparer."""

from typing import List, Dict, Any

from sqlalchemy.orm import Session

from app.models import Role
from seeds.preparers.base import BasePreparer

class RolePreparer(BasePreparer):
    """Preparer for Role model."""

    @property
    def table_name(self) -> str:
        return "roles"

    def prepare(self, db: Session, data: List[Dict[str, Any]]) -> List[Role]:
        """
        Prepare Role objects from raw data.

        Args:
            db: Database session (not used in roles, but required by interface)
            data: List of role dictionaries

        Returns:
            List of Role instances
        """

        return [
            Role(role=item.get("role"))
            for item in data
        ]