
"""
Utility module for handling PDF files.
"""
import logging
from pypdf import PdfReader

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted text content.
        
    Raises:
        Exception: If the file cannot be read or text cannot be extracted.
    """
    try:
        reader = PdfReader(file_path)
        text = []
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text.append(content)
        return "\n".join(text)
    except Exception as e:
        logger.error(f"Error extracting PDF text: {e}")
        raise e
