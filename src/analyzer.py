
"""
Module for local text analysis.
Provides functions to calculate basic statistics like word count, character count, and line count.
"""

def get_text_statistics(text: str) -> dict:
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
    # Remove empty lines from line count calculation if desired, 
    # but practically we usually count splitlines length or non-empty lines.
    # Requirement says "Righe nel testo". Standard wc count includes newlines.
    # Let's clean empty lines for specific behavior or keep all?
    # prompt says "Calcolo locale di parole, caratteri e righe nel testo"
    # standard python split() handles words by whitespace.
    
    return {
        "word_count": len(text.split()),
        "char_count": len(text),
        "line_count": len(lines)
    }
