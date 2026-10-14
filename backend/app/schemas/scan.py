from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ScanCreateText(BaseModel):
    text: str = Field(..., min_length=3, description="Visible text from webpage or UI component to scan")
    language: str = Field("auto", description="Target language: auto, en, hi, ta")

class ScanCreateUrl(BaseModel):
    url: str = Field(..., description="Accessible public e-commerce web URL")
    language: str = Field("auto", description="Target language: auto, en, hi, ta")

class FindingSchema(BaseModel):
    id: str
    scan_id: str
    category: str
    severity: str
    confidence: float
    text_snippet: str
    dom_selector: Optional[str] = None
    rationale: str
    consumer_impact: str
    ccpa_clause: str
    ccpa_category: str
    recommendation: str
    is_reviewed: bool

    class Config:
        from_attributes = True

class ScanResponse(BaseModel):
    id: str
    url: Optional[str] = None
    scan_type: str
    language: str
    status: str
    risk_score: float
    risk_category: str
    findings_count: int
    created_at: datetime
    fetch_method: Optional[str] = "http_client"
    content_length_analyzed: Optional[int] = 0
    page_title: Optional[str] = None
    warnings: Optional[List[str]] = []
    findings: List[FindingSchema] = []

    class Config:
        from_attributes = True
