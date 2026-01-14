
import pytest
from src.analyzer import get_text_statistics

def test_get_text_statistics_empty():
    """Test statistics for empty string."""
    stats = get_text_statistics("")
    assert stats["word_count"] == 0
    assert stats["char_count"] == 0
    assert stats["line_count"] == 0

def test_get_text_statistics_simple():
    """Test statistics for a simple sentence."""
    text = "Hello world"
    stats = get_text_statistics(text)
    assert stats["word_count"] == 2
    assert stats["char_count"] == 11
    assert stats["line_count"] == 1

def test_get_text_statistics_multiline():
    """Test statistics for multiline text."""
    text = "Hello\nWorld\nAgain"
    stats = get_text_statistics(text)
    assert stats["word_count"] == 3
    assert stats["char_count"] == 17  # 'Hello' (5) + \n (1) + 'World' (5) + \n (1) + 'Again' (5) = 17
    assert stats["line_count"] == 3

def test_get_text_statistics_whitespace():
    """Test statistics with extra whitespace."""
    text = "   Hello    world   "
    stats = get_text_statistics(text)
    assert stats["word_count"] == 2
    assert stats["char_count"] == 20
    assert stats["line_count"] == 1

def test_get_text_statistics_special_chars():
    """Test statistics with special characters."""
    text = "Hello, world! 123"
    stats = get_text_statistics(text)
    assert stats["word_count"] == 3
    # Check simple tokenization behavior
