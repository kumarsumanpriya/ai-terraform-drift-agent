import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from drift_agent.state_parser import TerraformStateParser
from drift_agent.drift_analyzer import DriftAnalyzer
from drift_agent.remediation_engine import RemediationEngine

console = Console()

@click.group()
def main():
    """🤖 Intelligent Terraform Drift Detection & AI Remediation Agent"""
    pass

@main.command()
@click.option("--state-file", required=True, help="Path to Terraform state JSON file")
@click.option("--report-output", default="drift_report.md", help="Markdown report destination")
def analyze(state_file: str, report_output: str):
    """Parses Terraform state, detects configuration drift, and produces remediation plan."""
    console.print(Panel.fit("[bold cyan]🤖 AI-Assisted Terraform Drift Analyzer[/bold cyan]\n[dim]Cross-referencing declared code against live cloud inventory[/dim]"))

    parser = TerraformStateParser(state_file)
    declared = parser.extract_resources()

    table = Table(title="📦 Declared Terraform Resources")
    table.add_column("Address", style="cyan")
    table.add_column("Type", style="magenta")

    for addr, res in list(declared.items())[:10]:
        table.add_row(addr, res.get("type", "unknown"))

    console.print(table)
    console.print(f"[bold green]✔ Successfully parsed {len(declared)} declared resources.[/bold green]")

    # Mock live query demonstration
    analyzer = DriftAnalyzer(declared_resources=declared, live_resources={})
    results = analyzer.analyze()
    report = RemediationEngine.generate_markdown_report(results)

    with open(report_output, "w", encoding="utf-8") as f:
        f.write(report)

    console.print(f"[bold green]✔ Drift remediation report written to {report_output}[/bold green]")

if __name__ == "__main__":
    main()
