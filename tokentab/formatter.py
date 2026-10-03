"""
Formatting and output export module for TokenTab.

Handles rich table rendering in the terminal and CSV file exports for benchmark results.
"""

from pathlib import Path
from typing import Sequence

import pandas as pd
from rich.console import Console
from rich.table import Table

from tokentab.benchmark import BenchmarkResult


def render_results_table(results: Sequence[BenchmarkResult]) -> None:
    """Render a styled Rich table summarizing benchmark results."""
    console = Console()
    table = Table(title="TokenTab LLM Benchmark Results", show_header=True, header_style="bold magenta")

    table.add_column("Provider", style="cyan", justify="left")
    table.add_column("Model", style="blue", justify="left")
    table.add_column("TTFT (s)", style="green", justify="right")
    table.add_column("Total Time (s)", style="yellow", justify="right")
    table.add_column("Prompt Tkn", style="white", justify="right")
    table.add_column("Comp Tkn", style="white", justify="right")
    table.add_column("Total Tkn", style="bold white", justify="right")
    table.add_column("Est. Cost ($)", style="bold green", justify="right")
    table.add_column("Estimated?", style="dim", justify="center")

    for r in results:
        table.add_row(
            r.provider.upper(),
            r.model,
            f"{r.ttft_sec:.3f}",
            f"{r.total_time_sec:.3f}",
            str(r.prompt_tokens),
            str(r.completion_tokens),
            str(r.total_tokens),
            f"${r.estimated_cost_usd:.6f}",
            "Yes" if r.token_usage_estimated else "No",
        )

    console.print()
    console.print(table)
    console.print()


def export_results_to_csv(results: Sequence[BenchmarkResult], output_path: str = "benchmark_results.csv") -> Path:
    """Export benchmark results to a CSV file using pandas."""
    data = [
        {
            "provider": r.provider,
            "model": r.model,
            "prompt": r.prompt,
            "ttft_sec": r.ttft_sec,
            "total_time_sec": r.total_time_sec,
            "prompt_tokens": r.prompt_tokens,
            "completion_tokens": r.completion_tokens,
            "total_tokens": r.total_tokens,
            "estimated_cost_usd": r.estimated_cost_usd,
            "token_usage_estimated": r.token_usage_estimated,
        }
        for r in results
    ]
    df = pd.DataFrame(data)
    path = Path(output_path)
    df.to_csv(path, index=False)
    return path
