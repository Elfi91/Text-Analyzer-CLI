
"""
Module for data persistence.
Handles saving and retrieving analysis results via StorageManager class.
"""
import json
import os
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class StorageManager:
    """Class to handle database operations (save/load)."""

    def __init__(self, data_dir: str = "data", db_filename: str = "db.json"):
        """
        Initializes the StorageManager.
        
        Args:
            data_dir (str): Directory to store data.
            db_filename (str): Name of the JSON database file.
        """
        self.data_dir = data_dir
        self.db_file = os.path.join(data_dir, db_filename)
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Ensures the data directory exists."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _load_db(self) -> list:
        """Loads the database from the JSON file."""
        if not os.path.exists(self.db_file):
            return []
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading database: {e}")
            return []

    def _save_db(self, data: list) -> None:
        """Saves the database to the JSON file."""
        try:
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Error saving database: {e}")

    def save_analysis(self, data: dict) -> str:
        """
        Saves a new analysis result to the database.

        Args:
            data (dict): The analysis data to save.

        Returns:
            str: The ID of the saved record.
        """
        record = data.copy()
        record["id"] = str(uuid.uuid4())
        record["timestamp"] = datetime.now().isoformat()
        
        current_db = self._load_db()
        current_db.append(record)
        self._save_db(current_db)
        
        logger.debug(f"Saved analysis record: {record['id']}")
        return record["id"]

    def get_history(self, limit: int = 5) -> list:
        """
        Retrieves the most recent analyses.
        """
        current_db = self._load_db()
        return current_db[-limit:][::-1]
