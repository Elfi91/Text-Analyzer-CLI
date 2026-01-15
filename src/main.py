
"""
Main entry point for the Text-Analyzer-CLI.
Orchestrates the CLI interface via the TextAnalyzerApp class.
"""
import sys
import os
import argparse
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from src.analyzer import TextAnalyzer
from src.storage import StorageManager
from src.ai_client import GeminiClient
from src.pdf_utils import PDFProcessor
from src.exporter import ReportExporter

# Configure Logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/app.log',
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TextAnalyzerApp:
    """Main Application Class."""

    def __init__(self, debug_mode: bool = False):
        """Initializes the application and its components."""
        self.console = Console()
        self.setup_logging(debug_mode)
        
        # Initialize Components
        self.analyzer = TextAnalyzer()
        self.storage = StorageManager()
        self.ai_client = GeminiClient()
        self.pdf_processor = PDFProcessor()
        self.exporter = ReportExporter()

    def setup_logging(self, debug_mode: bool):
        """Configures logging based on the debug flag."""
        if debug_mode:
            logging.getLogger().setLevel(logging.DEBUG)
            self.console.print("[yellow]DEBUG MODE ENABLED[/yellow]")
            logger.debug("Debug mode enabled.")

    def show_header(self):
        """Displays the application header."""
        self.console.print(Panel.fit(
            "[bold cyan]Text Analyzer CLI[/bold cyan]",
            border_style="cyan"
        ))

    def perform_analysis(self, text: str, source: str = "Input"):
        """Orchestrates the analysis process."""
        if not text or not text.strip():
            rprint("[bold red]Error:[/bold red] Input text is empty.")
            return

        rprint(f"\n[bold]Analyzing {source}...[/bold]")

        # 1. Local Analysis
        try:
            local_stats = self.analyzer.analyze(text)
            logger.debug(f"Local stats: {local_stats}")
        except Exception as e:
            logger.error(f"Local analysis failed: {e}")
            rprint(f"[bold red]Local Analysis Failed:[/bold red] {e}")
            return

        # 2. AI Analysis
        ai_result = {"sentiment": "SKIPPED", "confidence": "None"}
        summary = "N/A"
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True
            ) as progress:
                progress.add_task(description="Consulting Gemini AI...", total=None)
                ai_result = self.ai_client.analyze_sentiment(text)
                summary = self.ai_client.generate_summary(text)
                logger.debug(f"AI result: {ai_result}, Summary: {summary}")
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            rprint(f"[bold red]AI Analysis Failed:[/bold red] {e}")

        # 3. Save to DB
        record = {
            "text": text[:100] + "..." if len(text) > 100 else text, 
            "full_text": text, 
            "summary": summary,
            **local_stats,
            **ai_result
        }
        
        try:
            record_id = self.storage.save_analysis(record)
            rprint(f"[green]Analysis saved (ID: {record_id[:8]})[/green]")
        except Exception as e:
            logger.error(f"DB Save failed: {e}")
            rprint(f"[red]Warning: Could not save to database.[/red]")

        # 4. Display Results
        self._display_results(local_stats, ai_result, summary)

    def _display_results(self, local_stats: dict, ai_result: dict, summary: str):
        """Helper to print results table."""
        table = Table(title="Analysis Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Words", str(local_stats.get("word_count", 0)))
        table.add_row("Characters", str(local_stats.get("char_count", 0)))
        table.add_row("Lines", str(local_stats.get("line_count", 0)))
        
        sentiment = ai_result.get("sentiment", "UNKNOWN")
        sentiment_color = "green" if sentiment == "POSITIVE" else "red" if sentiment == "NEGATIVE" else "yellow"
        table.add_row("Sentiment", f"[{sentiment_color}]{sentiment}[/{sentiment_color}]")
        table.add_row("Confidence", ai_result.get("confidence", "Unknown"))
        table.add_row("AI Summary", summary, style="italic")

        self.console.print(table)

    def show_history(self):
        """Displays the analysis history."""
        try:
            history = self.storage.get_history(limit=5)
            if not history:
                rprint("[yellow]No history found.[/yellow]")
                return

            table = Table(title="Recent Analysis History")
            table.add_column("Timestamp", style="dim")
            table.add_column("Snippet")
            table.add_column("Sentiment")

            for record in history:
                sentiment = record.get("sentiment", "N/A")
                color = "green" if sentiment == "POSITIVE" else "red" if sentiment == "NEGATIVE" else "yellow"
                snippet = record.get("text", "")
                
                table.add_row(
                    record.get("timestamp", "")[:19],
                    snippet,
                    f"[{color}]{sentiment}[/{color}]"
                )
            
            self.console.print(table)
        except Exception as e:
            logger.error(f"Error showing history: {e}")
            rprint(f"[red]Error retrieving history: {e}[/red]")

    def run_interactive_menu(self):
        """Runs the main interactive loop."""
        self.show_header()
        while True:
            self.console.print("\n[bold]Main Menu[/bold]")
            self.console.print("1. [cyan]Analizza Testo[/cyan] 📝")
            self.console.print("2. [cyan]Vedi Storico[/cyan] 📜")
            self.console.print("3. [cyan]Esporta Dati[/cyan] 💾")
            self.console.print("4. [red]Esci[/red] ❌")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"], default="1")

            if choice == "1":
                self._handle_analysis_input()
            elif choice == "2":
                self.show_history()
            elif choice == "3":
                self._handle_export_menu()
            elif choice == "4":
                if Confirm.ask("Are you sure you want to exit?"):
                    rprint("[bold cyan]Goodbye![/bold cyan] 👋")
                    break
            
            input("\nPress Enter to continue...")

    def _handle_analysis_input(self):
        """Handles text/file input for analysis."""
        rprint("[dim]Tips: Supporta .txt e .pdf (testo selezionabile). Max consigliato: <100 pagine.[/dim]")
        text_input = Prompt.ask("Enter text to analyze (or file path)")
        clean_input = text_input.strip().strip("'").strip('"')
        
        if os.path.isfile(clean_input) or (sys.platform != "win32" and ("/" in clean_input or "." in clean_input)): 
             expanded_path = os.path.expanduser(clean_input)
             if os.path.exists(expanded_path):
                 try:
                     if expanded_path.lower().endswith(".pdf"):
                         rprint(f"[cyan]Detected PDF file: {expanded_path}[/cyan]")
                         content = self.pdf_processor.extract_text(expanded_path)
                         self.perform_analysis(content, source=f"PDF: {os.path.basename(expanded_path)}")
                     else:
                         with open(expanded_path, "r", encoding="utf-8") as f:
                             self.perform_analysis(f.read(), source=f"File: {os.path.basename(expanded_path)}")
                     return
                 except Exception as e:
                     rprint(f"[red]Error reading file: {e}[/red]")
        
        self.perform_analysis(text_input)

    def _handle_export_menu(self):
        """Handles the export file menu."""
        rprint("\n[bold]Export Options[/bold]")
        rprint("1. [cyan]Export to CSV[/cyan] 📊")
        rprint("2. [cyan]Export to Markdown[/cyan] 📝")
        rprint("3. [green]Export to Google Sheet[/green] ☁️")
        rprint("4. [dim]Cancel[/dim]")
        
        exp_choice = Prompt.ask("Choose format", choices=["1", "2", "3", "4"], default="1")
        
        if exp_choice in ["1", "2", "3"]:
            try:
                history = self.storage.get_history(limit=100)
                if not history:
                    rprint("[yellow]No history to export.[/yellow]")
                else:
                    if exp_choice == "1":
                        path = self.exporter.to_csv(history)
                        rprint(f"[green]Successfully exported CSV to:[/green] {path}")
                    elif exp_choice == "2":
                        path = self.exporter.to_markdown(history)
                        rprint(f"[green]Successfully exported Markdown to:[/green] {path}")
                    elif exp_choice == "3":
                        sheet_name = Prompt.ask("Enter Google Sheet Name")
                        url = self.exporter.to_google_sheet(history, sheet_name)
                        rprint(f"[green]Successfully exported to:[/green] {url}")
                        
            except Exception as e:
                rprint(f"[red]Export failed: {e}[/red]")

    def run(self):
        """Entry point for argument parsing and app execution."""
        parser = argparse.ArgumentParser(description="Text Analyzer CLI powered by Gemini AI")
        parser.add_argument("--text", help="Text string to analyze directly")
        parser.add_argument("--file", help="Path to a text file to analyze")
        parser.add_argument("--debug", action="store_true", help="Enable debug logging")
        
        args = parser.parse_args()
        
        # If created with specific debug flag in init, we might want to respect it or args.
        # But here we instantiate with args.debug
        
        # Re-init app if needed or just setup logging? 
        # Since __init__ is called when creating the object, let's create it here.
        # But we need args first.
        
        # Actually, self.__init__ already called setup_logging. But we didn't pass debug_mode there if we create app before main().
        # Let's create app inside main logic.
        pass # Logic moved to main block below

def main():
    parser = argparse.ArgumentParser(description="Text Analyzer CLI powered by Gemini AI")
    parser.add_argument("--text", help="Text string to analyze directly")
    parser.add_argument("--file", help="Path to a text file to analyze")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()

    app = TextAnalyzerApp(debug_mode=args.debug)

    if args.text:
        app.perform_analysis(args.text, source="CLI Argument")
    elif args.file:
        try:
            if args.file.lower().endswith(".pdf"):
                content = app.pdf_processor.extract_text(args.file)
                app.perform_analysis(content, source=f"PDF: {args.file}")
            else:
                with open(args.file, "r", encoding="utf-8") as f:
                    app.perform_analysis(f.read(), source=f"File: {args.file}")
        except FileNotFoundError:
             rprint(f"[bold red]Error:[/bold red] File not found: {args.file}")
    else:
        app.run_interactive_menu()

if __name__ == "__main__":
    main()
