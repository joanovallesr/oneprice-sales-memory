import asyncio

import pytest

import config
from analysis import _load_oneprice_tone, _openai_client, _vcon_to_text
from oneprice_sales_server import (
    _demo_search_response,
    _demo_search_results,
    search_by_intent,
)


def test_vcon_to_text_includes_all_context() -> None:
    vcon = {
        "subject": "Explorer lead",
        "dialog": [{"body": "Customer wants a third row."}],
        "analysis": [{"body": "Payment sensitive."}],
    }

    text = _vcon_to_text(vcon)

    assert "Explorer lead" in text
    assert "third row" in text
    assert "Payment sensitive" in text


def test_vcon_to_text_empty_fallback() -> None:
    assert _vcon_to_text({}) == "(no content)"


def test_oneprice_tone_file_is_loaded() -> None:
    tone = _load_oneprice_tone()

    assert "OnePrice" in tone
    assert "no haggle" in tone.lower()


def test_demo_results_are_labeled_synthetic() -> None:
    results = _demo_search_results("payment under 600")

    assert len(results) == 1
    assert results[0]["vcon_uuid"].startswith("demo-uuid-")
    assert results[0]["funnel_stage"] == "new_lead"
    assert results[0]["urgency"] == "hot_lead"
    assert "Synthetic" in results[0]["summary"]


def test_demo_response_never_claims_live_results() -> None:
    result = _demo_search_response("payment", "upstream error")

    assert result["demo"] is True
    assert result["live_search_succeeded"] is False
    assert "not real leads" in result["note"].lower()


def test_search_by_intent_rejects_non_positive_days() -> None:
    result = asyncio.run(search_by_intent("payment", days=0))

    assert result["success"] is False


def test_openai_client_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "OPENAI_API_KEY", "")

    with pytest.raises(ValueError):
        _openai_client()


def test_stdio_args_parsing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "VCON_MCP_STDIO_ARGS", "run, -i, image")

    assert config.get_vcon_stdio_args() == ["run", "-i", "image"]
