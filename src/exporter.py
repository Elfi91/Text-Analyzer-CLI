
"""
Module for exporting analysis data to various formats (CSV, Markdown).
"""
import csv
import logging
import os
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

def export_to_csv(data: List[Dict], filename: str = "export_history.csv") -> str:
    """
    Exports a list of analysis records to a CSV file.
    
    Args:
        data (list): List of dictionaries containing analysis data.
        filename (str): Target filename.
        
    Returns:
        str: Absolute path of the created file.
    """
    if not data:
        logger.warning("No data to export.")
        return ""
        
    try:
        # Determine fields from the first record
        fieldnames = list(data[0].keys())
        
        # Ensure we don't save huge full texts in CSV if not needed, 
        # but requirements say "export results". Let's keep it simple.
        
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        logger.info(f"Exported {len(data)} records to {filename}")
        return os.path.abspath(filename)
    except Exception as e:
        logger.error(f"CSV export failed: {e}")
        raise e

def export_to_markdown(data: List[Dict], filename: str = "export_history.md") -> str:
    """
    Exports a list of analysis records to a Markdown file.
    """
    if not data:
        return ""
        
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Analysis History Export\n\n")
            f.write(f"Generated on: {datetime.now().isoformat()}\n\n")
            
            for record in data:
                f.write(f"## ID: {record.get('id', 'N/A')}\n")
                f.write(f"**Date:** {record.get('timestamp')}\n\n")
                f.write(f"**Sentiment:** {record.get('sentiment')} ({record.get('confidence')})\n")
                f.write(f"**Stats:** {record.get('word_count')} words, {record.get('line_count')} lines.\n\n")
                
                # Show snippet of text
                text_snippet = record.get('text', '')
                f.write("### Text Snippet\n")
                f.write(f"> {text_snippet}\n\n")
                f.write("---\n\n")
                
        logger.info(f"Exported {len(data)} records to {filename}")
        return os.path.abspath(filename)
    except Exception as e:
        logger.error(f"Markdown export failed: {e}")
        raise e
