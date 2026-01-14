
"""
Module for exporting analysis data to various formats (CSV, Markdown).
"""
import csv
import logging
import os
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

EXPORT_DIR = "exports"

def _ensure_export_dir():
    """Ensures the export directory exists."""
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

def export_to_csv(data: List[Dict], filename: str = "export_history.csv") -> str:
    """
    Exports a list of analysis records to a CSV file.
    """
    if not data:
        logger.warning("No data to export.")
        return ""
        
    _ensure_export_dir()
    filepath = os.path.join(EXPORT_DIR, filename)

    try:
        # Determine fields from the first record
        fieldnames = list(data[0].keys())
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        logger.info(f"Exported {len(data)} records to {filepath}")
        return os.path.abspath(filepath)
    except Exception as e:
        logger.error(f"CSV export failed: {e}")
        raise e

def export_to_markdown(data: List[Dict], filename: str = "export_history.md") -> str:
    """
    Exports a list of analysis records to a Markdown file.
    """
    if not data:
        return ""
        
    _ensure_export_dir()
    filepath = os.path.join(EXPORT_DIR, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
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
                
        logger.info(f"Exported {len(data)} records to {filepath}")
        return os.path.abspath(filepath)
    except Exception as e:
        logger.error(f"Markdown export failed: {e}")
        raise e

import gspread


def export_to_google_sheet(data: List[Dict], sheet_name: str, credentials_path: str = None) -> str:
    """
    Exports data to a Google Sheet.
    
    Args:
        data (list): List of analysis records.
        sheet_name (str): Name of the Google Sheet (must be shared with service account).
        credentials_path (str): Path to credentials. Defaults to env var or 'credentials.json'.
        
    Returns:
        str: URL of the spreadsheet.
    """
    if not data:
        return ""
        
    # Resolve credentials path
    if not credentials_path:
        credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found at: {credentials_path}. See GOOGLE_SETUP.md")

    try:
        # Authenticate
        gc = gspread.service_account(filename=credentials_path)
        
        # Open Sheet
        try:
            sh = gc.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            raise ValueError(f"Spreadsheet '{sheet_name}' not found. Did you share it with the bot email?")

        worksheet = sh.get_worksheet(0) # Use the first sheet
        
        # Prepare headers and rows
        headers = list(data[0].keys())
        rows = []
        for record in data:
            row = []
            for value in record.values():
                # Truncate to 30k chars to be safe (Sheet limit is 50k)
                if isinstance(value, str) and len(value) > 30000:
                    row.append(value[:30000] + "... [TRUNCATED]")
                else:
                    row.append(value)
            rows.append(row)
        
        # Clear and write
        worksheet.clear()
        worksheet.append_row(headers)
        worksheet.append_rows(rows)
        
        logger.info(f"Exported to Google Sheet: {sheet_name}")
        return f"https://docs.google.com/spreadsheets/d/{sh.id}"
        
    except Exception as e:
        logger.error(f"Google Sheet export failed: {e}")
        raise e
