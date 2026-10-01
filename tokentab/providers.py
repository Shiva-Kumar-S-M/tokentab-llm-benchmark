"""
Provider configuration for TokenTab.

Models chosen (free tier as of 2026):
  - Groq:   llama-3.1-8b-instant  (OpenAI-compatible via api.groq.com)
  - Gemini: gemini-1.5-flash       (OpenAI-compatible via generativelanguage.googleapis.com)

Pricing is per 1 million tokens (USD). Free-tier quotas apply.
Groq: $0.05 input / $0.08 output per 1M tokens (llama-3.1-8b-instant).
Gemini: $0.075 input / $0.30 output per 1M tokens (gemini-1.5-flash, up to 128k ctx).
"""

PROVIDERS: dict[str, dict] = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
        "model": "llama-3.1-8b-instant",
        "price_input_per_1m": 0.05,
        "price_output_per_1m": 0.08,
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "api_key_env": "GEMINI_API_KEY",
        "model": "gemini-1.5-flash",
        "price_input_per_1m": 0.075,
        "price_output_per_1m": 0.30,
    },
}
