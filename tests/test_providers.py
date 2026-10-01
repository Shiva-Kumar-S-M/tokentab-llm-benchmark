"""
Unit tests for provider configurations.
"""

from tokentab.providers import PROVIDERS


def test_providers_structure():
    assert "groq" in PROVIDERS
    assert "gemini" in PROVIDERS


def test_provider_keys():
    for name, config in PROVIDERS.items():
        assert "base_url" in config
        assert "api_key_env" in config
        assert "model" in config
        assert "price_input_per_1m" in config
        assert "price_output_per_1m" in config
        assert isinstance(config["price_input_per_1m"], (int, float))
        assert isinstance(config["price_output_per_1m"], (int, float))
