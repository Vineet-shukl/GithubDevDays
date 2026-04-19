"""
Pydantic models for the Phishing Email Classifier.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EmailInput(BaseModel):
    """Input model for email analysis requests."""
    raw_email: str = Field(..., min_length=10)
    sender: str | None = None
    subject: str | None = None


class ThreatReport(BaseModel):
    """Structured threat analysis report."""
    is_phishing: bool
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    attack_type: Literal[
        "credential_harvesting",
        "malware_link", 
        "business_email_compromise",
        "fake_invoice",
        "none"
    ]
    severity: Literal["low", "medium", "high", "critical"]
    red_flags: list[str]
    spoofed_brand: str | None
    recommended_action: str
    explanation: str


class AnalysisResponse(BaseModel):
    """API response wrapper for threat reports."""
    report: ThreatReport
    analyzed_at: str
    model_used: str = "groq:llama-3.3-70b-versatile"
