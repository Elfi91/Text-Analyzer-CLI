
import os
import json
import pytest
from src.storage import StorageManager

@pytest.fixture
def mock_storage(tmp_path):
    """Fixture to create a StorageManager with a temp directory."""
    d = tmp_path / "subdir"
    # StorageManager creates dir if it doesn't exist
    return StorageManager(data_dir=str(d), db_filename="test_db.json")

def test_save_analysis(mock_storage):
    """Test saving a new analysis record."""
    data = {"text": "Test input", "word_count": 2}
    record_id = mock_storage.save_analysis(data)
    
    assert record_id is not None
    assert os.path.exists(mock_storage.db_file)
    
    with open(mock_storage.db_file, "r") as f:
        content = json.load(f)
    
    assert len(content) == 1
    saved_record = content[0]
    assert saved_record["id"] == record_id
    assert saved_record["text"] == "Test input"
    assert "timestamp" in saved_record

def test_get_history(mock_storage):
    """Test retrieving history."""
    # Save multiple records
    mock_storage.save_analysis({"text": "First"})
    mock_storage.save_analysis({"text": "Second"})
    mock_storage.save_analysis({"text": "Third"})
    
    history = mock_storage.get_history(limit=2)
    
    assert len(history) == 2
    assert history[0]["text"] == "Third"  # Most recent first
    assert history[1]["text"] == "Second"

def test_load_empty_db_file_not_exists(tmp_path):
    """Test retrieving history when DB file doesn't exist."""
    # Create manual instance in new dir
    d = tmp_path / "empty_dir"
    storage = StorageManager(data_dir=str(d))
    
    history = storage.get_history()
    assert history == []
