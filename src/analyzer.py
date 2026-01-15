
"""
Module for local text analysis.
Provides the TextAnalyzer class to calculate basic statistics.
"""

class TextAnalyzer:
    """Class for performing local text analysis."""

    def analyze(self, text: str) -> dict:
        """
        Calculates basic statistics for the given text.

        Args:
            text (str): The input text to analyze.

        Returns:
            dict: A dictionary containing:
                - 'word_count' (int): The number of words.
                - 'char_count' (int): The number of characters.
                - 'line_count' (int): The number of lines.
        """
        if not text:
            return {
                "word_count": 0,
                "char_count": 0,
                "line_count": 0
            }

        lines = text.splitlines()
        
        return {
            "word_count": len(text.split()),
            "char_count": len(text),
            "line_count": len(lines)
        }
