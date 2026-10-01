"""
CLI entrypoint for TokenTab.

Parses arguments, loads environment variables, runs benchmarks across providers,
and prints output table / saves CSV results.
"""

import argparse
import sys
from typing import List, Optional

from dotenv import load_dotenv
from rich.console import Console

from tokentab.benchmark import BenchmarkResult, run_single_benchmark
from tokentab.formatter import export_results_to_csv, render_results_table
from tokentab.providers import PROVIDERS

console = Console()

DEFAULT_PROMPTS = [
    "Explain quantum computing in 2 simple sentences.",
    "Write a 4-line poem about open source software.",
]


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="tokentab",
        description="Benchmark TTFT, total latency, token usage and cost across Groq and Gemini.",
    )
    parser.add_argument(
        "--prompt",
        "-p",
        type=str,
        help="Custom prompt to send to LLM providers.",
    )
    parser.add_argument(
        "--providers",
        nargs="+",
        default=list(PROVIDERS.keys()),
        choices=list(PROVIDERS.keys()),
        help="Providers to benchmark (default: groq gemini).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="benchmark_results.csv",
        help="Output CSV filepath (default: benchmark_results.csv).",
    )
    return parser.parse_args(args)


def main(argv: Optional[List[str]] = None) -> None:
    """Main CLI execution flow."""
    load_dotenv()
    parsed = parse_args(argv)

    prompts = [parsed.prompt] if parsed.prompt else DEFAULT_PROMPTS
    results: List[BenchmarkResult] = []

    console.print("[bold cyan]🚀 Starting TokenTab LLM Benchmark...[/bold cyan]")

    for prompt in prompts:
        console.print(f"\n[bold yellow]Prompt:[/bold yellow] [italic]'{prompt}'[/italic]")
        for provider_key in parsed.providers:
            console.print(f"  → Running benchmark on [bold magenta]{provider_key}[/bold magenta]...")
            try:
                res = run_single_benchmark(provider_key, prompt)
                results.append(res)
            except Exception as e:
                console.print(f"  [bold red]✖ Error running {provider_key}: {e}[/bold red]")

    if results:
        render_results_table(results)
        csv_path = export_results_to_csv(results, parsed.output)
        console.print(f"[bold green]✔ Results saved to {csv_path.resolve()}[/bold green]")
    else:
        console.print("[bold red]No benchmark results collected.[/bold red]")


if __name__ == "__main__":
    main(sys.argv[1:])
