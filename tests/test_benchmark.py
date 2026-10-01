"""
Unit tests for benchmark logic with mocked OpenAI streaming responses.
"""

from unittest.mock import MagicMock
from tokentab.benchmark import (
    calculate_cost,
    estimate_tokens_fallback,
    run_single_benchmark,
)


def test_calculate_cost():
    # Groq: $0.05 / 1M input, $0.08 / 1M output
    # 1000 input tokens = 0.00005, 1000 output tokens = 0.00008 -> total 0.00013
    cost = calculate_cost("groq", 1000, 1000)
    assert cost == 0.00013


def test_estimate_tokens_fallback():
    text = "Hello world this is a test prompt"  # 7 words
    tokens = estimate_tokens_fallback(text)
    assert tokens > 0
    assert tokens == int(7 * 1.33)


def test_run_single_benchmark_mocked():
    mock_client = MagicMock()

    # Mock chunk stream with usage
    chunk1 = MagicMock()
    chunk1.choices = [MagicMock()]
    chunk1.choices[0].delta.content = "Hello "
    chunk1.usage = None

    chunk2 = MagicMock()
    chunk2.choices = [MagicMock()]
    chunk2.choices[0].delta.content = "world!"
    chunk2.usage = MagicMock()
    chunk2.usage.prompt_tokens = 10
    chunk2.usage.completion_tokens = 5

    mock_client.chat.completions.create.return_value = [chunk1, chunk2]

    res = run_single_benchmark("groq", "Test prompt", client=mock_client)

    assert res.provider == "groq"
    assert res.prompt == "Test prompt"
    assert res.prompt_tokens == 10
    assert res.completion_tokens == 5
    assert res.total_tokens == 15
    assert res.token_usage_estimated is False
    assert res.ttft_sec >= 0
    assert res.total_time_sec >= 0
