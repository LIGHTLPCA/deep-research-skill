"""
Command Line Interface for Deep Research Skill.
Usage:
    deep-research "Topic to research" [--out report.md] [--json]
"""

import sys
import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

# Ensure UTF-8 stdout on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from .lpca_bridge import PHASE_LABELS, TOTAL_PHASES, DeepResearchAgent


def confidence_style(score: float) -> str:
    """Green >=80%, yellow >=50%, red below."""
    if score >= 80:
        return "bold green"
    if score >= 50:
        return "bold yellow"
    return "bold red"


def confidence_display(report) -> tuple:
    """Returns (rendered_score, style). Unmeasurable scores render as N/A."""
    if not report.has_evidence:
        return "[bold red]N/A[/bold red] [dim](no sources retrieved)[/dim]", "bold red"
    style = confidence_style(report.confidence_score)
    return f"[{style}]{report.confidence_score}%[/{style}]", style


def build_summary(report, failed_queries) -> Panel:
    """Renders the final stats as a bordered panel with a colored score badge."""
    score_text, style = confidence_display(report)

    table = Table.grid(padding=(0, 2))
    table.add_column(justify="right", style="dim")
    table.add_column()
    table.add_row("Confidence Score", score_text)
    table.add_row("Verified Claims", str(report.verified_claim_count))
    table.add_row("Active Citations", str(report.citation_count))

    if failed_queries:
        dims = ", ".join(sorted({sq.dimension for sq in failed_queries}))
        table.add_row(
            "Warning",
            f"[yellow]{len(failed_queries)} search vector(s) returned no results[/yellow]\n"
            f"[dim]({dims}) - the search engine may be rate limiting requests.[/dim]",
        )

    title = "[bold]Research Complete[/bold]" if report.has_evidence else "[bold]Research Failed[/bold]"

    return Panel(
        table,
        title=title,
        border_style=style,
        expand=False,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Deep Research Skill — Anti-Hallucination Research Engine CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  deep-research "Quantum Computing Error Correction 2026"
  deep-research "Large Language Model Benchmarks" --out research.md
  python -m lpca_deep_research.cli "Autonomous AI Agents" --json
""",
    )
    parser.add_argument("topic", type=str, help="Research topic or question to investigate")
    parser.add_argument("-o", "--out", type=str, help="Output file path for generated report (.md)")
    parser.add_argument("--json", action="store_true", help="Output result in structured JSON format")
    parser.add_argument("--queries", type=int, default=1, help="Max search queries per dimension (default: 1)")

    args = parser.parse_args()

    console = Console(stderr=True)
    console.print("[bold]Deep Research Engine[/bold]")
    console.print(f"Topic: [cyan]{escape(args.topic)}[/cyan]\n")

    agent = DeepResearchAgent(max_queries_per_dimension=args.queries)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(f"[1/{TOTAL_PHASES}] Starting...", total=None)

        def on_progress(phase, detail="", advance=0, total=None):
            if total is not None:
                progress.update(task, total=total)
            label = PHASE_LABELS[phase - 1]
            description = f"[{phase}/{TOTAL_PHASES}] {label}"
            if detail:
                # Dimension labels like "[overview]" would parse as rich markup
                description += f" {escape(detail)}"
            progress.update(task, description=description, advance=advance)

        report = agent.run(args.topic, on_progress=on_progress)

    console.print(build_summary(report, agent.failed_queries))
    console.print()

    if args.json:
        payload = agent.to_json(report)
        json_output = json.dumps(payload, indent=2)
        if args.out:
            Path(args.out).write_text(json_output, encoding="utf-8")
            print(f"Report saved to {args.out}")
        else:
            print(json_output)
    else:
        if args.out:
            Path(args.out).write_text(report.markdown_content, encoding="utf-8")
            print(f"Report saved to {args.out}")
        else:
            print("=" * 60)
            print(report.markdown_content)
            print("=" * 60)


if __name__ == "__main__":
    main()
