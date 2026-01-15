
"""
Utility module for handling PDF files via PDFProcessor class.
"""
import logging
from pypdf import PdfReader

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Class to handle PDF processing tasks."""

    def extract_text(self, file_path: str) -> str:
        """
        Extracts text from a PDF file.

        Args:
            file_path (str): Path to the PDF file.
            
        Returns:
            str: Extracted text content.
        """
        try:
            reader = PdfReader(file_path)
            text = []
            for i, page in enumerate(reader.pages):
                try:
                    content = page.extract_text()
                    if content:
                        text.append(content)
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {i} (layout mode): {e}")
                    try:
                        content = page.extract_text(extraction_mode="plain")
                        if content:
                            text.append(content)
                    except Exception as e2:
                        logger.error(f"Failed to extract text from page {i} (fallback mode): {e2}")
                        continue
            return "\n".join(text)
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            raise e
