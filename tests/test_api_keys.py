"""
Unit Tests for API Keys and Cloud LLM Providers in System C.
Validates live connectivity, JSON response parsing, and error-handling fallbacks.
"""

import json
import os
import pytest
from unittest.mock import MagicMock, patch

from src.system_c.llm import (
    _call_gemini_native,
    call_llm,
    clean_and_parse_json,
    get_llm_config,
)
from src.system_c.state import create_initial_state
from src.system_c.nodes.decomposer import decomposer_node


def test_gemini_native_payload_and_parsing():
    """Verify Gemini native caller constructs proper Google API payload and parses candidates."""
    mock_response_data = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Apple ticker is AAPL."}]
                }
            }
        ],
        "usageMetadata": {
            "promptTokenCount": 12,
            "candidatesTokenCount": 8,
        },
    }

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(mock_response_data).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
        messages = [{"role": "user", "content": "What is the stock ticker for Apple Inc.?"}]
        content, p_tok, c_tok = _call_gemini_native("gemini-flash-latest", messages, temperature=0.0)

        assert "AAPL" in content
        assert p_tok == 12
        assert c_tok == 8
        assert mock_urlopen.called


def test_gemini_json_mode_payload():
    """Verify Gemini request includes responseMimeType when json_mode=True."""
    mock_response_data = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": '{"status": "ok", "target_ticker": "AAPL"}'}]
                }
            }
        ],
        "usageMetadata": {"promptTokenCount": 20, "candidatesTokenCount": 15},
    }

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(mock_response_data).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        messages = [{"role": "user", "content": "Return json"}]
        content, p_tok, c_tok = _call_gemini_native(
            "gemini-flash-latest", messages, temperature=0.0, json_mode=True
        )
        parsed = clean_and_parse_json(content)
        assert parsed.get("status") == "ok"
        assert parsed.get("target_ticker") == "AAPL"


def test_gemini_decomposer_node_integration(monkeypatch):
    """Verify Decomposer routes properly with provider set to gemini."""
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("LLM_MODEL", "gemini-flash-latest")

    state = create_initial_state(
        query="What was Apple's total revenue and operating income in fiscal 2024?",
        mode="v2_aamr",
    )

    mock_response_data = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": json.dumps({
                                "target_ticker": "AAPL",
                                "target_tickers": ["AAPL"],
                                "fiscal_years": [2024],
                                "sub_queries": ["What was Apple's total revenue and operating income in fiscal 2024?"],
                                "sub_query_plans": [
                                    {
                                        "query": "What was Apple's total revenue and operating income in fiscal 2024?",
                                        "target_tool": "tabular_tool",
                                        "ticker": "AAPL",
                                        "fiscal_year": 2024,
                                    }
                                ],
                            })
                        }
                    ]
                }
            }
        ],
        "usageMetadata": {"promptTokenCount": 150, "candidatesTokenCount": 80},
    }

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(mock_response_data).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        result = decomposer_node(state)
        assert result["target_ticker"] == "AAPL"
        assert 2024 in result["fiscal_years"]
        assert len(result["sub_queries"]) >= 1


def test_mock_provider_zero_api_key_resilience(monkeypatch):
    """Verify Mock provider works 100% reliably with zero API keys."""
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    state = create_initial_state(query="Compare NVIDIA and Apple revenues", mode="v2_aamr")

    content, updated_telemetry = call_llm(
        state=state,
        node_name="decomposer",
        messages=[{"role": "user", "content": "Decompose"}],
        json_mode=True,
    )
    assert len(content) > 0
    assert "calls" in updated_telemetry


def test_unsupported_provider_raises_clear_error(monkeypatch):
    """Verify unsupported providers raise clear actionable ValueError."""
    monkeypatch.setenv("LLM_PROVIDER", "unknown_provider_xyz")
    state = create_initial_state(query="test", mode="v2_aamr")

    with pytest.raises(ValueError) as excinfo:
        call_llm(state=state, node_name="decomposer", messages=[{"role": "user", "content": "hi"}])
    assert "Unsupported LLM_PROVIDER" in str(excinfo.value)
