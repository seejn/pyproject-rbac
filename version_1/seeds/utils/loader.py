"""Data loading utilities."""

import json
from pathlib import Path
from typing import List, Dict, Any

from seeds.utils.logger import get_logger

logger = get_logger(__name__)

class DataLoader:
    """Handles loading JSON data files."""

    def __init__(self, data_folder: Path):
        """
        Initialize data loader.

        Args:   
            data_folder: Path to folder containing JSON data files
        """
        self.data_folder = data_folder

        if not self.data_folder.exists():
            raise FileNotFoundError(f"Data folder not found: {self.data_folder}")

    def load_json_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Load a single JSON file.

        Args:
            file_path: Path to JSON file

        Returns: 
            Parsed JSON data
        """

        try: 
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Loaded data from {file_path.name}")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path.name}: {e}")
        except Exception as e:
            logger.error(f"Error loading {file_path.name}: {e}")

    def load_data(self, file_patterns: List[str]) -> List[Dict[str, Any]]:
        """
        Load multiple JSON files matching patterns.

        Args:
            file_patterns: List of file patterns to match (e.g. , ['policies', 'roles', 'permissions'])

        Returns:
            List of loaded data dictionaries
        """
        all_data = []
        
        for pattern in file_patterns:
            json_files = list(self.data_folder.glob(f'{pattern}.json'))

            if not json_files:
                logger.warning(f"No files found matching patterns: {patterns}.json")
                continue

            for json_file in json_files:
                data = self.load_json_file(json_file)
                all_data.append(data)

        return all_data
        