
"""
Module for exporting analysis data via ReportExporter class.
"""
import csv
import logging
import os
from datetime import datetime
from typing import List, Dict
import gspread

logger = logging.getLogger(__name__)

class ReportExporter:
    """Class to handle exporting data to various formats."""

    def __init__(self, export_dir: str = "exports"):
        """
        Initializes the ReportExporter.

        Args:
            export_dir (str): Directory where local exports are saved.
        """
        self.export_dir = export_dir
        self._ensure_export_dir()

    def _ensure_export_dir(self):
        """Ensures the export directory exists."""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def to_csv(self, data: List[Dict], filename: str = "export_history.csv") -> str:
        """
        Exports a list of analysis records to a CSV file.
        """
        if not data:
            logger.warning("No data to export.")
            return ""
            
        filepath = os.path.join(self.export_dir, filename)

        try:
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

    def to_markdown(self, data: List[Dict], filename: str = "export_history.md") -> str:
        """
        Exports a list of analysis records to a Markdown file.
        """
        if not data:
            return ""
            
        filepath = os.path.join(self.export_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("# Analysis History Export\n\n")
                f.write(f"Generated on: {datetime.now().isoformat()}\n\n")
                
                for record in data:
                    f.write(f"## ID: {record.get('id', 'N/A')}\n")
                    f.write(f"**Date:** {record.get('timestamp')}\n\n")
                    f.write(f"**Sentiment:** {record.get('sentiment')} ({record.get('confidence')})\n")
                    f.write(f"**Stats:** {record.get('word_count')} words, {record.get('line_count')} lines.\n\n")
                    
                    text_snippet = record.get('text', '')
                    f.write("### Text Snippet\n")
                    f.write(f"> {text_snippet}\n\n")
                    f.write("---\n\n")
                    
            logger.info(f"Exported {len(data)} records to {filepath}")
            return os.path.abspath(filepath)
        except Exception as e:
            logger.error(f"Markdown export failed: {e}")
            raise e

    def to_google_sheet(self, data: List[Dict], sheet_name: str, credentials_path: str = None) -> str:
        """
        Exports data to a Google Sheet.
        """
        if not data:
            return ""
            
        if not credentials_path:
            credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Credentials file not found at: {credentials_path}. See GOOGLE_SETUP.md")

        try:
            gc = gspread.service_account(filename=credentials_path)
            
            try:
                sh = gc.open(sheet_name)
            except gspread.SpreadsheetNotFound:
                raise ValueError(f"Spreadsheet '{sheet_name}' not found. Did you share it with the bot email?")

            worksheet = sh.get_worksheet(0)
            
            headers = list(data[0].keys())
            rows = []
            for record in data:
                row = []
                for value in record.values():
                    if isinstance(value, str) and len(value) > 30000:
                        row.append(value[:30000] + "... [TRUNCATED]")
                    else:
                        row.append(value)
                rows.append(row)
            
            worksheet.clear()
            worksheet.append_row(headers)
            worksheet.append_rows(rows)

            logger.info(f"Exported to Google Sheet: {sheet_name}")
            return f"https://docs.google.com/spreadsheets/d/{sh.id}"
            
        except Exception as e:
            logger.error(f"Google Sheet export failed: {e}")
            raise e
