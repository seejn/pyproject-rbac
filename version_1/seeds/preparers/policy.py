"""policy data preparer."""

from typing import List, Dict, Any

from sqlalchemy.orm import Session

from app.models import Policy
from seeds.preparers.base import BasePreparer

class PolicyPreparer(BasePreparer):
    """Preparer for Policy model."""

    @property
    def table_name(self) -> str:
        return "policies"

    def prepare(self, db: Session, data: List[Dict[str, Any]]) -> List[Policy]:
        """
        Prepare Policy objects from raw data.

        Args:
            db: Database session (not used in policies, but required by interface)
            data: List of policy dictionaries

        Returns:
            List of Policy instances
        """
        
        return [
            Policy(
                policy_name=item.get("policy_name"),
                category=item.get("category"),
                action=item.get("action")
            )
            for item in data
        ]