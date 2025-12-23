"""Base preparer class."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from sqlalchemy.orm import Session

class BasePreparer(ABC):
    """Abstract base class for data preparers."""

    @abstractmethod
    def prepare(self, db: Session, data: List[Dict[str, Any]]) -> List[Any]:
        """
        Prepare new data into model instances.
        
        Args:
            db: Database session
            data: Raw data from JSON

        Returns:
            List of model instances
        """
        pass

    @property
    @abstractmethod
    def table_name(self) -> str:
        """Return the table name this preparer handles."""
        pass