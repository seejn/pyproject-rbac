"""Main entry point for running seeder as a module.

Usage:
    python -m seeds
    python -m seeds --model Policy,Role
"""

import argparse
import sys
from pathlib import Path

from seeds.core.seeder import Seeder
from seeds.utils.logger import get_logger

logger = get_logger(__name__)

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Database seeder for populating initial data"
    )

    parser.add_argument(
        "--model",
        help="Comma-separated list of model names to seed (e.g., 'Policy,Role')",
        type=str
    )
    parser.add_argument(
        "--dry-run",
        help="Run without committing changes to database",
        action="store_true"
    )
    return parser.parse_args()

def main():
    """Main entry point for the seeder."""
    args = parse_arguments()

    models = [m.strip() for m in args.model.split(",")] if args.model else None

    logger.info(f"Starting seeder for models: {models or 'all'}")

    seeder = Seeder(models=models, dry_run=args.dry_run)
    seeder.run()

    logger.info("Seeding process completed")

if __name__ == "__main__":
    main()