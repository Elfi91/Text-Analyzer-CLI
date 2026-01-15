
import pytest
from src.analyzer import TextAnalyzer

@pytest.fixture
def analyzer():
    return TextAnalyzer()

def test_get_text_statistics_empty(analyzer):
    """Test statistics for empty string."""
    stats = analyzer.analyze("")
    assert stats["word_count"] == 0
    assert stats["char_count"] == 0
    assert stats["line_count"] == 0

def test_get_text_statistics_simple(analyzer):
    """Test statistics for a simple sentence."""
    text = "Hello world"
    stats = analyzer.analyze(text)
    assert stats["word_count"] == 2
    assert stats["char_count"] == 11
    assert stats["line_count"] == 1

def test_get_text_statistics_multiline(analyzer):
    """Test statistics for multiline text."""
    text = "Hello\nWorld\nAgain"
    stats = analyzer.analyze(text)
    assert stats["word_count"] == 3
    assert stats["char_count"] == 17
    assert stats["line_count"] == 3

def test_get_text_statistics_whitespace(analyzer):
    """Test statistics with extra whitespace."""
    text = "   Hello    world   "
    stats = analyzer.analyze(text)
    assert stats["word_count"] == 2
    assert stats["char_count"] == 20
    assert stats["line_count"] == 1

def test_get_text_statistics_special_chars(analyzer):
    """Test statistics with special characters."""
    text = "Hello, world! 123"
    stats = analyzer.analyze(text)
    assert stats["word_count"] == 3
