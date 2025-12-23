"""Database session management."""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from seeds.utils.logger import get_logger

logger = get_logger(__name__)

@contextmanager
def get_db_session(dry_run: bool = False) -> Generator[Session, None, None]:
    """
    Context manager for database session handling.

    Args:
        dry_run: If True, rollback instead of commit

    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db

        if dry_run: 
            logger.info("Dry run mode: Rolling back changes")
            db.rollback()
        else:
            db.commit()
            logger.info("Changes committed to database")

    except Exception as e:
        logger.error(f"Session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()