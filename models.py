"""
Pydantic models for OpenAI analysis results.
"""
# pyright: reportMissingImports=false
from pydantic import BaseModel
from pydantic.fields import Field
from typing import Optional


class AnalysisResult(BaseModel):
    """Structured output from OpenAI classify_lead (analysis.py)."""
    funnel_stage: str = Field(description="One of: new_lead, appointment_set, in_store, pending_finance, sold, lost")
    urgency: str = Field(description="One of: hot_lead, warm_lead, cold_lead")
    vehicle_interest: Optional[str] = None
    payment_sensitive: bool = False
    shopping_competitors: bool = False
    price_shock: bool = False
    needs_manager_followup: bool = False
    timeline: Optional[str] = None
    summary: Optional[str] = None
