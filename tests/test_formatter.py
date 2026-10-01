"""
Unit tests for table formatting and CSV export logic.
"""

from pathlib import Path
from tokentab.benchmark import BenchmarkResult
from tokentab.formatter import export_results_to_csv, render_results_table


def test_export_results_to_csv(tmp_path: Path):
    sample_result = BenchmarkResult(
        provider="groq",
        model="llama-3.1-8b-instant",
        prompt="Test prompt",
        ttft_sec=0.123,
        total_time_sec=0.456,
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
        estimated_cost_usd=0.000005,
        token_usage_estimated=False,
    )

    out_file = tmp_path / "test_out.csv"
    res_path = export_results_to_csv([sample_result], str(out_file))

    assert res_path.exists()
    content = res_path.read_text()
    assert "groq" in content
    assert "llama-3.1-8b-instant" in content
    assert "0.123" in content


def test_render_results_table_runs_without_error():
    sample_result = BenchmarkResult(
        provider="gemini",
        model="gemini-1.5-flash",
        prompt="Sample",
        ttft_sec=0.2,
        total_time_sec=0.8,
        prompt_tokens=5,
        completion_tokens=15,
        total_tokens=20,
        estimated_cost_usd=0.000010,
        token_usage_estimated=True,
    )

    # Should execute without throwing exception
    render_results_table([sample_result])
