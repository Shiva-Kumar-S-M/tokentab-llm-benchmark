"""
Benchmark execution module for TokenTab.

Handles streaming chat completion API calls to OpenAI-compatible endpoints,
measuring TTFT (time-to-first-token), total latency, token usage, and estimating cost.
Retries transient API errors using tenacity.
"""

import os
import time
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI, APIError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from tokentab.providers import PROVIDERS


@dataclass
class BenchmarkResult:
    provider: str
    model: str
    prompt: str
    ttft_sec: float
    total_time_sec: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    token_usage_estimated: bool


def calculate_cost(provider_key: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate total estimated cost based on per-1M token rates."""
    config = PROVIDERS.get(provider_key, {})
    price_in = config.get("price_input_per_1m", 0.0)
    price_out = config.get("price_output_per_1m", 0.0)

    cost_in = (prompt_tokens / 1_000_000.0) * price_in
    cost_out = (completion_tokens / 1_000_000.0) * price_out
    return round(cost_in + cost_out, 6)


def estimate_tokens_fallback(text: str) -> int:
    """Fallback token estimation based on word count (~1.33 tokens per word)."""
    words = len(text.split())
    return max(1, int(words * 1.33))


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((APIError, TimeoutError, ConnectionError)),
    reraise=True,
)
def _create_stream_with_retry(client: OpenAI, model: str, prompt: str):
    """Helper function to initiate chat completion stream with tenacity retry."""
    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        stream_options={"include_usage": True},
    )


def run_single_benchmark(
    provider_key: str,
    prompt: str,
    client: Optional[OpenAI] = None,
) -> BenchmarkResult:
    """
    Execute a streaming chat completion call for a single provider and prompt.
    Measures TTFT and total duration. Extracts or estimates token counts.
    Retries API errors up to 3 times with exponential backoff.
    """
    if provider_key not in PROVIDERS:
        raise ValueError(f"Unknown provider '{provider_key}'. Available: {list(PROVIDERS.keys())}")

    config = PROVIDERS[provider_key]
    api_key = os.environ.get(config["api_key_env"], "mock_key")

    if client is None:
        client = OpenAI(
            base_url=config["base_url"],
            api_key=api_key,
        )

    start_time = time.perf_counter()
    first_token_time: Optional[float] = None
    accumulated_text = ""
    prompt_tokens = 0
    completion_tokens = 0
    token_usage_estimated = False

    stream = _create_stream_with_retry(client, config["model"], prompt)

    for chunk in stream:
        if chunk.choices and len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                accumulated_text += delta.content

        if hasattr(chunk, "usage") and chunk.usage:
            prompt_tokens = chunk.usage.prompt_tokens or 0
            completion_tokens = chunk.usage.completion_tokens or 0

    end_time = time.perf_counter()
    total_time_sec = end_time - start_time
    ttft_sec = (first_token_time - start_time) if first_token_time else total_time_sec

    if prompt_tokens == 0 and completion_tokens == 0:
        token_usage_estimated = True
        prompt_tokens = estimate_tokens_fallback(prompt)
        completion_tokens = estimate_tokens_fallback(accumulated_text)

    total_tokens = prompt_tokens + completion_tokens
    cost = calculate_cost(provider_key, prompt_tokens, completion_tokens)

    return BenchmarkResult(
        provider=provider_key,
        model=config["model"],
        prompt=prompt,
        ttft_sec=round(ttft_sec, 4),
        total_time_sec=round(total_time_sec, 4),
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        estimated_cost_usd=cost,
        token_usage_estimated=token_usage_estimated,
    )
