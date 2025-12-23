"""Main seeder class."""

from pathlib import Path
from typing import List, Optional, Dict, Any

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from seeds.constants import MODEL_MAPPING, SEED_ORDER
from seeds.core.session import get_db_session
from seeds.preparers import PREPARERS
from seeds.utils.loader import DataLoader
from seeds.utils.logger import get_logger

logger = get_logger(__name__)

class Seeder:
    """Database seeder for populating tables with initial data."""

    def __init__(self, models: Optional[List[str]] = None, dry_run: bool = False):
        """
        Initialize the seeder.

        Args:
            models: List of model names to seed. If None, seeds all models.
            dry_run: If True, rollback changes instead of committing
        """
        self.models = models
        self.dry_run = dry_run
        self.data_folder = Path(__file__).parent.parent / 'data'
        self.loader = DataLoader(self.data_folder)

    def get_file_patterns(self) -> List[str]:
        """
        Get list of the file patterns to load based on selected models.

        Returns:
            List of file patterns
        """
        if not self.models:
            return ['*']

        patterns = [
            MODEL_MAPPING.get(model)
            for model in self.models
            if MODEL_MAPPING.get(model)
        ]

        if not patterns:
            logger.warning(f"No valid models found in: {self.models}")

        return patterns or ["*"]
    
    def order_seed_data(self, seed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Order seed data based on SEED_ORDER to handle foreign key dependencies.

        Args: 
            seed_data: Unordered seed data

        Returns:
            Ordered seed data
        """
        data_by_table = {
            item.get("table_name"): item
            for item in seed_data
        }

        ordered_tables = set(SEED_ORDER)
        ordered_data = []

        for table in SEED_ORDER:
            logger.info(f"ordering for table '{table}'.")
            if table in data_by_table:
                ordered_data.append(data_by_table[table])
            else:
                logger.debug(f"Table '{table}' in SEED_ORDER but no data provided")

        for table_name, item in data_by_table.items():
            if table_name not in ordered_tables:
                logger.warning(
                    f"Table '{table_name}' not in SEED_ORDER, adding at end"
                )
                ordered_data.append(item)


        return ordered_data

    def seed_table(self, db, table_data: Dict[str, Any]) -> bool:
        """
        Seed a single table with data

        Args:
            db: Database session
            table_data: Dictionary containing table_name and data

        Returns:
            True if successful, False otherwise
        """
        table_name = table_data.get("table_name")
        data = table_data.get("data", [])

        if not data:
            logger.info(f"No data to seed for table '{table_name}'")
            return True

        preparer = PREPARERS.get(table_name)
        if not preparer:
            logger.warning(f"No preparer found for table '{table_name}'")
            return False

        try: 
            model_data = preparer.prepare(db, data)

            if not model_data:
                logger.info(f"No records prepared for table '{table_name}'")
                return True

            db.bulk_save_objects(model_data)
            db.flush()

            logger.info(f"Successfully seeded {len(model_data)} records into '{table_name}'")
            return True
        except IntegrityError as e:
            logger.error(f"Integrity error seeding '{table_name}': {e.orig}")
            return False
        except SQLAlchemyError as e:
            logger.error(f"Database error seeding '{table_name}': {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error seeding '{table_name}: {e}'")
            return False
    
    def run(self) -> None:
        """Execute the seeding process."""
        try:
            file_patterns = self.get_file_patterns()
            seed_data = self.loader.load_data(file_patterns)

            if not seed_data:
                logger.warning(f"No data files found to seed")
                return 

            ordered_data = self.order_seed_data(seed_data)

            with get_db_session(dry_run=self.dry_run) as db:
                success_count = 0
                fail_count = 0

                for table_data in ordered_data:
                    if self.seed_table(db, table_data):
                        success_count += 1
                    else:
                        fail_count += 1

                logger.info(
                    f"Seeding complete: {success_count} successful, {fail_count} failed"
                )

                if self.dry_run:
                    logger.info("Dry run completed - no changes were committed")
                
        except Exception as e:
            logger.error(f"Fatal error during seeding: {e}")
            raise