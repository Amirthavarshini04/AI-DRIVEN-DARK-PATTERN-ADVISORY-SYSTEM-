from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Finding, RemediationAttempt
from app.schemas.compliance import RemediationGenerateRequest, RemediationVerifyRequest, RemediationResponse
from app.remediation.engine import generate_remediation_alternative, verify_remediation

router = APIRouter()

@router.post("/remediation/generate")
def generate_remediation(payload: RemediationGenerateRequest, db: Session = Depends(get_db)):
    finding = db.query(Finding).filter(Finding.id == payload.finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail=f"Finding '{payload.finding_id}' not found.")
    
    proposed, rationale, fixable = generate_remediation_alternative(finding.text_snippet, finding.category)
    verification = verify_remediation(finding.text_snippet, proposed, finding.category)

    attempt = RemediationAttempt(
        finding_id=finding.id,
        original_text=finding.text_snippet,
        proposed_text=proposed,
        rationale=rationale,
        before_risk=verification["before_risk"],
        after_risk=verification["after_risk"],
        status=verification["status"],
        is_verified=verification["is_verified"]
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "id": attempt.id,
        "finding_id": finding.id,
        "original_text": attempt.original_text,
        "proposed_text": attempt.proposed_text,
        "rationale": attempt.rationale,
        "before_risk": attempt.before_risk,
        "after_risk": attempt.after_risk,
        "status": attempt.status,
        "is_verified": attempt.is_verified,
        "risk_drop": round(attempt.before_risk - attempt.after_risk, 1)
    }

@router.post("/remediation/verify")
def custom_verify_remediation(payload: RemediationVerifyRequest, db: Session = Depends(get_db)):
    finding = db.query(Finding).filter(Finding.id == payload.finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail=f"Finding '{payload.finding_id}' not found.")
    
    verification = verify_remediation(finding.text_snippet, payload.proposed_text, finding.category)

    attempt = RemediationAttempt(
        finding_id=finding.id,
        original_text=finding.text_snippet,
        proposed_text=payload.proposed_text,
        rationale="User-provided alternative wording verification",
        before_risk=verification["before_risk"],
        after_risk=verification["after_risk"],
        status=verification["status"],
        is_verified=verification["is_verified"]
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "id": attempt.id,
        "finding_id": finding.id,
        "original_text": attempt.original_text,
        "proposed_text": attempt.proposed_text,
        "rationale": attempt.rationale,
        "before_risk": attempt.before_risk,
        "after_risk": attempt.after_risk,
        "status": attempt.status,
        "is_verified": attempt.is_verified,
        "risk_drop": verification["risk_drop"]
    }
