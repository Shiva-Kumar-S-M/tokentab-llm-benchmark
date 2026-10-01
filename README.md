# TokenTab ⚡ (`tokentab-llm-benchmark`)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**TokenTab** is a lightweight Python CLI tool that sends identical prompts to multiple LLM providers (Groq and Gemini via their OpenAI-compatible REST endpoints) and measures key performance and financial metrics:
- **TTFT** (Time-To-First-Token) in seconds
- **Total Latency** in seconds
- **Token Counts** (Prompt, Completion, Total)
- **Estimated Cost** in USD based on per-million token pricing

---

## 🤖 Models Chosen & Pricing

TokenTab uses free-tier models accessible via OpenAI-compatible endpoints:

| Provider | Model Name | Endpoint URL | Free-Tier Pricing (per 1M tokens) |
| :--- | :--- | :--- | :--- |
| **Groq** | `llama-3.1-8b-instant` | `https://api.groq.com/openai/v1` | **$0.05** input / **$0.08** output |
| **Gemini** | `gemini-1.5-flash` | `https://generativelanguage.googleapis.com/v1beta/openai` | **$0.075** input / **$0.30** output |

---

## ⚡ Streaming & Token Usage Note

TokenTab requests usage statistics directly within OpenAI-compatible streaming chunks (`stream_options={"include_usage": True}`).

If a provider endpoint does not report token usage in the streaming chunks:
- TokenTab automatically falls back to an **estimated token count** based on word count (~1.33 tokens per word).
- The terminal output and exported CSV clearly indicate whether token usage was exact or estimated (`token_usage_estimated=True`).

---

## 🚀 Quickstart

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Shiva-Kumar-S-M/tokentab-llm-benchmark.git
cd tokentab-llm-benchmark
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### 2. Environment Configuration

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 💻 CLI Usage

Run the default benchmark across both providers:

```bash
python -m tokentab
```

Or pass a custom prompt and specify output CSV path:

```bash
python -m tokentab --prompt "Compare microservices vs monoliths in 3 sentences." --output results.csv
```

### Options

- `-p, --prompt`: Custom prompt string to benchmark.
- `--providers`: List of providers to include (`groq`, `gemini`). Default: `groq gemini`.
- `-o, --output`: CSV file path for exporting results. Default: `benchmark_results.csv`.

---

## 🧪 Testing & Code Quality

Run tests (all tests mock API responses and perform zero network requests):

```bash
pytest
```

Run linting with Ruff:

```bash
ruff check .
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
