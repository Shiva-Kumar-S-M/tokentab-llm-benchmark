"""
Provider configuration for TokenTab.

Models chosen (free tier as of 2026):
  - Groq:   llama-3.1-8b-instant  (OpenAI-compatible via api.groq.com)
  - Gemini: gemini-1.5-flash       (OpenAI-compatible via generativelanguage.googleapis.com)
"""

PROVIDERS: dict[str, dict] = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
        "model": "llama-3.1-8b-instant",
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "api_key_env": "GEMINI_API_KEY",
        "model": "gemini-1.5-flash",
    },
}
