import pytest
from pydantic import ValidationError

from models import AnalysisResult


def test_analysis_result_defaults() -> None:
    result = AnalysisResult(funnel_stage="new_lead", urgency="warm_lead")

    assert result.vehicle_interest is None
    assert result.payment_sensitive is False
    assert result.shopping_competitors is False
    assert result.price_shock is False
    assert result.needs_manager_followup is False
    assert result.timeline is None
    assert result.summary is None


def test_analysis_result_requires_core_fields() -> None:
    with pytest.raises(ValidationError):
        AnalysisResult()


def test_analysis_result_serializes_to_json() -> None:
    result = AnalysisResult(
        funnel_stage="new_lead",
        urgency="hot_lead",
        vehicle_interest="Explorer",
        payment_sensitive=True,
        summary="Synthetic test lead.",
    )

    payload = result.model_dump_json()

    assert '"funnel_stage":"new_lead"' in payload
    assert '"payment_sensitive":true' in payload
