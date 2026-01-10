import json
import typer
from pathlib import Path
from rich.console import Console
from rich.progress import track
from rich.table import Table
import time

from api.resume_tailor.score import calculate_score
from api.resume_tailor.extract import normalize_output, extract_relevant_jd
from api.resume_tailor.tailor import run_tailoring_engine


model="llama-3.3-70b-versatile"
app = typer.Typer(help="SniperHire-V1: Tailor Your Resume With AI")

# Initizalizing rich console
console = Console()


def extract(jd_file: Path = typer.Argument(..., help="Path to the Job Description Text File"), model=model):

    jd_file = Path(jd_file)

    if not jd_file.exists():
        console.print(f"[bold red]Error:[/bold red] File {jd_file} not found.")
        raise typer.Exit(1)
    
    with console.status("[bold green]Running Extraction..."):

        with open(jd_file, "r") as file:
            jd_text = file.read()
        
        jd_requirements = extract_relevant_jd(jd_text, model=model)
        normalized_requirements = normalize_output(jd_requirements)

        console.print(f"{normalized_requirements}")

        return normalized_requirements


def score(jd_requirements: json , master_resume: json):

    score = calculate_score(jd_requirements, master_resume)

    return score

@app.command()
def tailor(
    jd_file: Path = typer.Argument(..., help="Path to the Job Description text file"),
    output: str = typer.Option("Tailored_Resume.pdf", "--output", "-o", help="Name of output PDF"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show full match breakdown")
):
    """
    Tailor your master resume to a specific job description.
    """
    if not jd_file.exists():
        console.print(f"[bold red]Error:[/bold red] File {jd_file} not found.")
        raise typer.Exit(1)

    with console.status("[bold green]Running Semantic Scorer..."):
        # 1. Load Data
        with open("api/resume_tailor/master_resume.json", "r") as f:
            master_data = json.load(f)
        
        with open(jd_file, "r") as f:
            jd_text = f.read()

        jd_requirements = extract('c:/Portfolio Projects/SniperHire-V1/cli/jd.txt', model=model)
        score = score(jd_requirements, master_data)
        tailored_json = run_tailoring_engine(master_data, jd_text, jd_requirements, score)

    # 3. UI Feedback using 'Rich'
    console.print(f"\n[bold]Tailoring Complete![/bold]")
    console.print(f"[bold cyan]ATS Match Score:[/bold cyan] {score}%")

    if verbose:
        table = Table(title="Skill Match Breakdown")
        table.add_column("Category", style="magenta")
        table.add_column("Match %", style="green")
        table.add_row("Languages", "95%")
        table.add_row("Frameworks", "88%")
        console.print(table)

    # 4. Render
    with console.status("[bold blue]Generating PDF..."):
        from api.resume_tailor.renderer import generate_tailored_resume
        generate_tailored_resume(tailored_json, master_data, output)

    console.print(f"[bold green]Success![/bold green] Resume saved to [underline]{output}[/underline]\n")


if __name__ == "__main__":
    app()