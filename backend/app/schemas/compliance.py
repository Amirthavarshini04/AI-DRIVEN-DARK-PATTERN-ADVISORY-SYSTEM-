from pydantic import BaseModel
from typing import List, Optional

class ComplianceGuidelineSchema(BaseModel):
    id: str
    category_code: str
    category_name: str
    clause_reference: str
    plain_explanation: str
    problematic_examples: List[str]
    compliant_alternative: str
    official_url: str
    last_reviewed: str

    class Config:
        from_attributes = True

class RemediationGenerateRequest(BaseModel):
    finding_id: str

class RemediationVerifyRequest(BaseModel):
    finding_id: str
    proposed_text: str

class RemediationResponse(BaseModel):
    id: str
    finding_id: str
    original_text: str
    proposed_text: str
    rationale: str
    before_risk: float
    after_risk: float
    status: str
    is_verified: bool
    risk_drop: float

class AnalyticsOverviewResponse(BaseModel):
    total_scans: int
    total_findings: int
    high_risk_pages_count: int
    avg_risk_score: float
    category_distribution: dict
    language_distribution: dict
    severity_distribution: dict
    recent_scans: List[dict]
