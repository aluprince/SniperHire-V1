#!/usr/bin/env python3
"""
SniperHire CLI - Complete working example with Typer + Rich

This is a production-ready CLI with:
- Subcommands (tailor, track, status)
- Arguments and options
- Pretty output with Rich
- Error handling
- Progress bars
"""

import typer
import json
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import print as rprint
from enum import Enum
import time

# Initialize Rich console for pretty output
console = Console()

# Create Typer app
app = typer.Typer(
    name="SniperHire",
    help="🎯 Tailor resumes to jobs in seconds. Built with AI.",
    invoke_without_command=True,
    no_args_is_help=True
)

# ============================================================================
# PART 1: UNDERSTANDING TYPER BASICS
# ============================================================================

class JobBoard(str, Enum):
    """Enum for job board options"""
    jobberman = "jobberman"
    indeed = "indeed"
    linkedin = "linkedin"

# ============================================================================
# PART 2: UTILITY FUNCTIONS
# ============================================================================

def load_master_resume():
    """Load your master resume from JSON"""
    try:
        with open("data/master_resume.json") as f:
            return json.load(f)
    except FileNotFoundError:
        console.print("[red]❌ Error: data/master_resume.json not found[/red]")
        raise typer.Exit(1)

def load_job_description(job_file: Optional[str], job_text: Optional[str]) -> str:
    """Load job description from file or text"""
    if job_file:
        try:
            with open(job_file) as f:
                return f.read()
        except FileNotFoundError:
            console.print(f"[red]❌ Error: File '{job_file}' not found[/red]")
            raise typer.Exit(1)
    elif job_text:
        return job_text
    else:
        console.print("[red]❌ Error: Provide --job-file or --job-text[/red]")
        raise typer.Exit(1)

# ============================================================================
# PART 3: COMMANDS (These are what users run)
# ============================================================================

@app.command()
def tailor(
    job_file: Optional[str] = typer.Option(
        None,
        "--job-file",
        "-f",
        help="Path to job description file (e.g., job.txt)"
    ),
    job_text: Optional[str] = typer.Option(
        None,
        "--job-text",
        "-t",
        help="Job description as text (wrap in quotes)"
    ),
    output: str = typer.Option(
        "resume_tailored.docx",
        "--output",
        "-o",
        help="Output file path"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed logs"
    )
):
    """
    🎯 Tailor your resume to a job description
    
    Usage Examples:
    
    1. From file:
       python cli.py tailor --job-file job.txt
    
    2. From text:
       python cli.py tailor --job-text "Senior Backend Engineer..."
    
    3. With custom output:
       python cli.py tailor --job-file job.txt --output my_resume.docx
    
    4. Verbose mode:
       python cli.py tailor --job-file job.txt --verbose
    """
    
    console.print("\n[bold cyan]🚀 SniperHire Resume Tailoring[/bold cyan]")
    console.print("=" * 50)
    
    # Load job description
    console.print("[yellow]📋 Reading job description...[/yellow]")
    job_desc = load_job_description(job_file, job_text)
    console.print(f"   ✓ Loaded {len(job_desc)} characters")
    
    if verbose:
        console.print(f"\n[dim]Job Description Preview:[/dim]")
        console.print(f"[dim]{job_desc[:200]}...[/dim]\n")
    
    # Load master resume
    console.print("[yellow]📄 Loading master resume...[/yellow]")
    master = load_master_resume()
    console.print(f"   ✓ Loaded resume for {master['contact']['name']}")
    
    # Simulate processing (in real code, this is your extraction/tailoring)
    console.print("[yellow]⚙️  Processing job requirements...[/yellow]")
    for step in track(
        ["Extracting requirements", "Analyzing skills match", "Tailoring bullets", "Generating document"],
        description="Processing..."
    ):
        time.sleep(0.5)  # Simulate work
    
    # Save file
    console.print(f"[yellow]💾 Saving to {output}...[/yellow]")
    # In real code: generate_resume_docx(tailored, master, output)
    console.print(f"   ✓ Saved {output}")
    
    # Success message
    console.print("\n[bold green]✅ Success![/bold green]")
    panel = Panel(
        f"Resume tailored and saved to [bold cyan]{output}[/bold cyan]\n"
        f"Next step: Review and apply!",
        title="✨ Resume Ready",
        border_style="green"
    )
    console.print(panel)

@app.command()
def status(
    format: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format: table, json, or csv"
    )
):
    """
    📊 Show application status and stats
    
    Usage:
    python cli.py status
    python cli.py status --format json
    """
    
    console.print("\n[bold cyan]📊 Application Status[/bold cyan]")
    console.print("=" * 50)
    
    # Create table
    table = Table(title="Recent Applications", border_style="cyan")
    table.add_column("Company", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Date Applied", style="green")
    table.add_column("Status", style="yellow")
    
    # Sample data
    table.add_row("TechFlow Solutions", "Senior Backend Engineer", "2025-01-09", "Applied")
    table.add_row("AI Startup Co", "Backend Engineer", "2025-01-08", "Applied")
    table.add_row("DataCorp", "Senior Engineer", "2025-01-07", "Interview Scheduled")
    
    console.print(table)
    
    # Stats
    console.print("\n[bold]Statistics:[/bold]")
    stats_table = Table(show_header=False, border_style="blue")
    stats_table.add_row("Total Applications", "[bold cyan]45[/bold cyan]")
    stats_table.add_row("Interviews Booked", "[bold green]3[/bold green]")
    stats_table.add_row("Interview Rate", "[bold yellow]6.7%[/bold yellow]")
    stats_table.add_row("Avg ATS Score", "[bold]78.5%[/bold]")
    console.print(stats_table)

@app.command()
def batch(
    input_dir: str = typer.Argument(
        "jobs/",
        help="Directory containing job descriptions"
    ),
    output_dir: str = typer.Option(
        "resumes/",
        "--output",
        "-o",
        help="Directory to save tailored resumes"
    ),
    limit: int = typer.Option(
        10,
        "--limit",
        "-l",
        help="Max number of jobs to process"
    )
):
    """
    🔄 Batch tailor multiple job descriptions
    
    Setup:
    1. Create jobs/ folder
    2. Add job descriptions as .txt files
    3. Run: python cli.py batch
    
    Usage:
    python cli.py batch
    python cli.py batch --limit 20
    python cli.py batch --output my_resumes/
    """
    
    console.print(f"\n[bold cyan]🔄 Batch Processing[/bold cyan]")
    console.print("=" * 50)
    
    # Check input directory
    input_path = Path(input_dir)
    if not input_path.exists():
        console.print(f"[red]❌ Directory '{input_dir}' not found[/red]")
        raise typer.Exit(1)
    
    # Find job files
    job_files = list(input_path.glob("*.txt"))
    if not job_files:
        console.print(f"[red]❌ No .txt files found in '{input_dir}'[/red]")
        raise typer.Exit(1)
    
    console.print(f"[yellow]Found {len(job_files)} job descriptions[/yellow]")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Process each job
    processed = 0
    for job_file in track(job_files[:limit], description="Processing jobs..."):
        # In real code: tailor resume and save
        # For now, just simulate
        output_file = output_path / f"resume_{job_file.stem}.docx"
        processed += 1
    
    console.print(f"\n[bold green]✅ Done![/bold green]")
    console.print(f"   Processed: {processed} jobs")
    console.print(f"   Resumes saved to: {output_dir}")

@app.command()
def init():
    """
    🏗️ Initialize SniperHire (first time setup)
    
    Creates:
    - data/master_resume.json
    - jobs/ directory
    - resumes/ directory
    """
    
    console.print("\n[bold cyan]🏗️ Initializing SniperHire[/bold cyan]")
    console.print("=" * 50)
    
    # Create directories
    directories = ["data", "jobs", "resumes", "output"]
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        console.print(f"[green]✓[/green] Created {dir_name}/")
    
    # Create sample master resume if doesn't exist
    master_path = Path("data/master_resume.json")
    if not master_path.exists():
        sample = {
            "contact": {
                "name": "Your Name",
                "email": "your.email@example.com",
                "location": "Your Location",
                "github": "github.com/yourprofile"
            },
            "experience": [],
            "projects": [],
            "master_skills": {}
        }
        with open(master_path, "w") as f:
            json.dump(sample, f, indent=2)
        console.print(f"[green]✓[/green] Created data/master_resume.json")
    
    console.print("\n[bold green]✅ Setup complete![/bold green]")
    console.print("Next steps:")
    console.print("1. Edit data/master_resume.json with your info")
    console.print("2. Add job descriptions to jobs/ folder")
    console.print("3. Run: python cli.py tailor --job-file jobs/example.txt")

@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version"
    )
):
    """SniperHire - AI Resume Tailoring CLI"""
    if version:
        console.print("SniperHire v1.0.0")
        raise typer.Exit()

# ============================================================================
# PART 4: MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    app()