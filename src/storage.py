
"""
Module for data persistence.
Handles saving and retrieving analysis results using a local JSON file.
"""
import json
import os
import uuid
from datetime import datetime
import logging


DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "db.json")

def _ensure_data_dir():
    """Ensures the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

logger = logging.getLogger(__name__)

def _load_db() -> list:
    """Loads the database from the JSON file."""
    _ensure_data_dir()
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading database: {e}")
        return []

def _save_db(data: list) -> None:
    """Saves the database to the JSON file."""
    _ensure_data_dir()
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        logger.error(f"Error saving database: {e}")

def save_analysis(data: dict) -> str:
    """
    Saves a new analysis result to the database.

    Args:
        data (dict): The analysis data to save. Expected keys:
                     'text', 'word_count', 'sentiment', etc.

    Returns:
        str: The ID of the saved record.
    """
    record = data.copy()
    record["id"] = str(uuid.uuid4())
    record["timestamp"] = datetime.now().isoformat()
    
    current_db = _load_db()
    current_db.append(record)
    _save_db(current_db)
    
    logger.debug(f"Saved analysis record: {record['id']}")
    return record["id"]

def get_history(limit: int = 5) -> list:
    """
    Retrieves the most recent analyses.

    Args:
        limit (int): The maximum number of records to return.

    Returns:
        list: A list of analysis records, most recent first.
    """
    current_db = _load_db()
    # Sort by timestamp descending (assuming appended in order, but safer to sort)
    # Using reverse list for efficiency if we assume append-only log structure
    # efficient enough for small DB.
    
    # Return last 'limit' items reversed
    return current_db[-limit:][::-1]
