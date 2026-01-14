
"""
Main entry point for the Text-Analyzer-CLI.
Orchestrates the CLI interface, local analysis, AI integration, and database storage.
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
from rich.layout import Layout
from rich import print as rprint

from src import analyzer
from src import storage
from src import ai_client
from src import pdf_utils
from src import exporter

# Configure Logging
logging.basicConfig(
    filename='app.log',
    level=logging.WARNING, # Default level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()

def setup_logging(debug_mode: bool):
    """Configures logging based on the debug flag."""
    if debug_mode:
        logging.getLogger().setLevel(logging.DEBUG)
        console.print("[yellow]DEBUG MODE ENABLED[/yellow]")
        logger.debug("Debug mode enabled.")

def show_header():
    """Displays the application header."""
    console.print(Panel.fit(
        "[bold cyan]Text Analyzer CLI[/bold cyan]",
        border_style="cyan"
    ))

def perform_analysis(text: str, source: str = "Input"):
    """
    Orchestrates the analysis process for a given text.
    
    1. Local Analysis (Word Count)
    2. AI Analysis (Sentiment)
    3. Save to DB
    4. Display Results
    """
    if not text or not text.strip():
        rprint("[bold red]Error:[/bold red] Input text is empty.")
        return

    rprint(f"\n[bold]Analyzing {source}...[/bold]")

    # 1. Local Analysis
    try:
        local_stats = analyzer.get_text_statistics(text)
        logger.debug(f"Local stats: {local_stats}")
    except Exception as e:
        logger.error(f"Local analysis failed: {e}")
        rprint(f"[bold red]Local Analysis Failed:[/bold red] {e}")
        return

    # 2. AI Analysis (with Spinner)
    ai_result = {"sentiment": "SKIPPED", "confidence": "None"}
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            progress.add_task(description="Consulting Gemini AI...", total=None)
            ai_result = ai_client.analyze_sentiment(text)
            logger.debug(f"AI result: {ai_result}")
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
        rprint(f"[bold red]AI Analysis Failed:[/bold red] {e}")

    # 3. Save to DB
    record = {
        "text": text[:100] + "..." if len(text) > 100 else text, # Store snippet or full? requirements say "salvato automaticamente". Snippet is safer for view, but logic might want full. Let's store full text but view snippet.
        # Wait, if text is huge, DB size explodes. Let's follow requirement: "persistenza". Assuming full text.
        "full_text": text, 
        **local_stats,
        **ai_result
    }
    
    try:
        record_id = storage.save_analysis(record)
        rprint(f"[green]Analysis saved (ID: {record_id[:8]})[/green]")
    except Exception as e:
        logger.error(f"DB Save failed: {e}")
        rprint(f"[red]Warning: Could not save to database.[/red]")

    # 4. Display Results
    table = Table(title="Analysis Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Words", str(local_stats["word_count"]))
    table.add_row("Characters", str(local_stats["char_count"]))
    table.add_row("Lines", str(local_stats["line_count"]))
    
    sentiment_color = "green" if ai_result.get("sentiment") == "POSITIVE" else "red" if ai_result.get("sentiment") == "NEGATIVE" else "yellow"
    table.add_row("Sentiment", f"[{sentiment_color}]{ai_result.get('sentiment', 'UNKNOWN')}[/{sentiment_color}]")
    table.add_row("Confidence", ai_result.get("confidence", "Unknown"))

    console.print(table)


def show_history():
    """Displays the analysis history."""
    try:
        history = storage.get_history(limit=5)
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
            snippet = record.get("text", "") # We decided to store snippet in 'text' key in verify logic? No, let's check storage.py. 
            # Storage.py just saves what we pass. In perform_analysis I put snippet in 'text' and full in 'full_text'. 
            # Ideally 'text' should be the text. Let's align. 
            # In perform_analysis I did: "text": text[:100]...
            
            table.add_row(
                record.get("timestamp", "")[:19], # Simple truncate isoformat
                snippet,
                f"[{color}]{sentiment}[/{color}]"
            )
        
        console.print(table)
    except Exception as e:
        logger.error(f"Error showing history: {e}")
        rprint(f"[red]Error retrieving history: {e}[/red]")


def interactive_menu():
    """Runs the main interactive loop."""
    while True:
        console.print("\n[bold]Main Menu[/bold]")
        console.print("1. [cyan]Analizza Testo[/cyan] 📝")
        console.print("2. [cyan]Vedi Storico[/cyan] 📜")
        console.print("3. [cyan]Esporta Dati[/cyan] 💾")
        console.print("4. [red]Esci[/red] ❌")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"], default="1")

        if choice == "1":
            rprint("[dim]Tips: Supporta .txt e .pdf (testo selezionabile). Max consigliato: <100 pagine.[/dim]")
            text_input = Prompt.ask("Enter text to analyze (or file path)")
            # Sanitize input (remove quotes often added by terminal drag-and-drop)
            clean_input = text_input.strip().strip("'").strip('"')
            
            # Check if it's a file
            if os.path.isfile(clean_input) or (sys.platform != "win32" and ("/" in clean_input or "." in clean_input)): 
                 # Try expanded path
                 expanded_path = os.path.expanduser(clean_input)
                 if os.path.exists(expanded_path):
                     try:
                         if expanded_path.lower().endswith(".pdf"):
                             rprint(f"[cyan]Detected PDF file: {expanded_path}[/cyan]")
                             content = pdf_utils.extract_text_from_pdf(expanded_path)
                             perform_analysis(content, source=f"PDF: {os.path.basename(expanded_path)}")
                         else:
                             with open(expanded_path, "r", encoding="utf-8") as f:
                                 perform_analysis(f.read(), source=f"File: {os.path.basename(expanded_path)}")
                         continue
                     except Exception as e:
                         rprint(f"[red]Error reading file: {e}[/red]")
            
            perform_analysis(text_input)

        elif choice == "2":
            show_history()
            
        elif choice == "3":
             # Export Menu
             rprint("\n[bold]Export Options[/bold]")
             rprint("1. [cyan]Export to CSV[/cyan] 📊")
             rprint("2. [cyan]Export to Markdown[/cyan] 📝")
             rprint("3. [dim]Cancel[/dim]")
             
             exp_choice = Prompt.ask("Choose format", choices=["1", "2", "3"], default="1")
             
             if exp_choice in ["1", "2"]:
                 try:
                     history = storage.get_history(limit=100) # Get more history for export
                     if not history:
                         rprint("[yellow]No history to export.[/yellow]")
                     else:
                         if exp_choice == "1":
                             path = exporter.export_to_csv(history)
                             rprint(f"[green]Successfully exported CSV to:[/green] {path}")
                         else:
                             path = exporter.export_to_markdown(history)
                             rprint(f"[green]Successfully exported Markdown to:[/green] {path}")
                 except Exception as e:
                     rprint(f"[red]Export failed: {e}[/red]")

        elif choice == "4":
            if Confirm.ask("Are you sure you want to exit?"):
                rprint("[bold cyan]Goodbye![/bold cyan] 👋")
                break
        
        input("\nPress Enter to continue...")


def main():
    parser = argparse.ArgumentParser(description="Text Analyzer CLI powered by Gemini AI")
    parser.add_argument("--text", help="Text string to analyze directly")
    parser.add_argument("--file", help="Path to a text file to analyze")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()

    setup_logging(args.debug)
    show_header()

    if args.text:
        perform_analysis(args.text, source="CLI Argument")
    elif args.file:
        try:
            if args.file.lower().endswith(".pdf"):
                content = pdf_utils.extract_text_from_pdf(args.file)
                perform_analysis(content, source=f"PDF: {args.file}")
            else:
                with open(args.file, "r", encoding="utf-8") as f:
                    perform_analysis(f.read(), source=f"File: {args.file}")
        except FileNotFoundError:
             rprint(f"[bold red]Error:[/bold red] File not found: {args.file}")
    else:
        # No args provided, launch interactive mode
        interactive_menu()

if __name__ == "__main__":
    main()
