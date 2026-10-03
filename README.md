# TokenTab

A lightweight Python CLI that benchmarks TTFT, total latency, token usage, and estimated cost across LLM providers.

## Overview

TokenTab sends identical prompts to multiple LLM providers (Groq and Gemini, via their OpenAI-compatible REST endpoints) and measures latency, token consumption, and estimated API cost. It is intended for developers evaluating provider performance, cost, or availability before committing to an integration.

## Features

- Streaming chat completions with measured time-to-first-token (TTFT) and total latency
- Token usage extraction from streaming chunks, with an automatic word-count-based fallback estimate
- Per-provider cost estimation from per-million-token pricing
- Rich terminal table output and CSV export of results
- Automatic retries with exponential backoff on transient API errors

### Models and Pricing

| Provider | Model | Endpoint | Pricing per 1M tokens |
| :--- | :--- | :--- | :--- |
| Groq | `llama-3.1-8b-instant` | `https://api.groq.com/openai/v1` | $0.05 input / $0.08 output |
| Gemini | `gemini-1.5-flash` | `https://generativelanguage.googleapis.com/v1beta/openai` | $0.075 input / $0.30 output |

### Token Usage Note

TokenTab requests usage statistics inside OpenAI-compatible streaming chunks (`stream_options={"include_usage": True}`). If a provider does not report usage in the stream, TokenTab falls back to an estimated token count (~1.33 tokens per word) and marks the result with `token_usage_estimated=True` in both the terminal output and the CSV export.

## Tech Stack

- Python 3.11+
- openai (OpenAI-compatible client)
- python-dotenv, rich, tenacity, pandas
- pytest, ruff

## Project Structure

```text
tokentab-llm-benchmark/
├── tokentab/
│   ├── __init__.py
│   ├── __main__.py      # python -m tokentab entry point
│   ├── benchmark.py     # streaming benchmark execution and metrics
│   ├── cli.py           # argument parsing and CLI flow
│   ├── formatter.py     # Rich table rendering and CSV export
│   └── providers.py     # provider endpoints, models, and pricing
├── tests/               # pytest suite (all API calls mocked)
├── .env.example
├── pyproject.toml
├── requirements.txt
└── LICENSE
```

## Prerequisites

- Python 3.11 or newer
- API keys for Groq and/or Gemini

## Installation

```bash
git clone https://github.com/Shiva-Kumar-S-M/tokentab-llm-benchmark.git
cd tokentab-llm-benchmark
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Description | Required |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | API key for the Groq endpoint | Yes, to benchmark Groq |
| `GEMINI_API_KEY` | API key for the Gemini endpoint | Yes, to benchmark Gemini |

If a key is missing, TokenTab emits a warning and falls back to a placeholder key for that provider.

## Usage

Run the default benchmark across both providers:

```bash
python -m tokentab
```

Run with a custom prompt and output path:

```bash
python -m tokentab --prompt "Compare microservices vs monoliths in 3 sentences." --output results.csv
```

The installed console script is equivalent:

```bash
tokentab --providers groq --output groq_results.csv
```

### Options

| Flag | Description | Default |
| :--- | :--- | :--- |
| `-p, --prompt` | Prompt to send to each provider | Two built-in prompts |
| `--providers` | Space-separated list of `groq` and/or `gemini` | `groq gemini` |
| `-o, --output` | CSV output path | `benchmark_results.csv` |

## Testing

```bash
pytest
```

All tests mock API responses and perform no network requests. Lint with:

```bash
ruff check .
```

## Roadmap

- Additional providers and configurable model selection via CLI flags
- Optional JSON export alongside CSV
- Aggregated statistics (mean/percentile latency) across repeated runs

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- Author: Shiva Kumar S.M
- GitHub: https://github.com/Shiva-Kumar-S-M
- Email: shivukumar.iu@gmail.com
