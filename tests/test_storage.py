
import os
import json
import pytest
from src import storage

# Mocking DB_FILE for tests to avoid writing to the real db.json
# We will use monkeypatch to point storage.DB_FILE to a temp file

@pytest.fixture
def mock_db_file(tmp_path, monkeypatch):
    """Fixture to mock the DB file path."""
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test_db.json"
    monkeypatch.setattr(storage, "DB_FILE", str(p))
    return p

def test_save_analysis(mock_db_file):
    """Test saving a new analysis record."""
    data = {"text": "Test input", "word_count": 2}
    record_id = storage.save_analysis(data)
    
    assert record_id is not None
    assert os.path.exists(mock_db_file)
    
    with open(mock_db_file, "r") as f:
        content = json.load(f)
    
    assert len(content) == 1
    saved_record = content[0]
    assert saved_record["id"] == record_id
    assert saved_record["text"] == "Test input"
    assert "timestamp" in saved_record

def test_get_history(mock_db_file):
    """Test retrieving history."""
    # Save multiple records
    storage.save_analysis({"text": "First"})
    storage.save_analysis({"text": "Second"})
    storage.save_analysis({"text": "Third"})
    
    history = storage.get_history(limit=2)
    
    assert len(history) == 2
    assert history[0]["text"] == "Third"  # Most recent first
    assert history[1]["text"] == "Second"

def test_load_empty_db_file_not_exists(mock_db_file):
    """Test retrieving history when DB file doesn't exist."""
    # Don't save anything, so file isn't created by save_analysis
    # But mock_db_file path is set.
    # Note: fixture creates directory but not file until we write
    
    history = storage.get_history()
    assert history == []
