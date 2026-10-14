from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Finding, UserFeedback
from app.schemas.finding import FeedbackCreate, FeedbackResponse

router = APIRouter()

@router.get("/findings")
def list_findings(
    severity: str = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    q = db.query(Finding)
    if severity:
        q = q.filter(Finding.severity == severity)
    if category:
        q = q.filter(Finding.category == category)
    return q.order_by(Finding.confidence.desc()).all()

@router.post("/findings/{finding_id}/feedback", response_model=FeedbackResponse)
def submit_finding_feedback(finding_id: str, payload: FeedbackCreate, db: Session = Depends(get_db)):
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail=f"Finding '{finding_id}' not found.")
    
    fb = UserFeedback(
        finding_id=finding.id,
        is_false_positive=payload.is_false_positive,
        comment=payload.comment
    )
    finding.is_reviewed = True
    db.add(fb)
    db.commit()
    db.refresh(fb)

    return {
        "id": fb.id,
        "finding_id": finding.id,
        "is_false_positive": fb.is_false_positive,
        "comment": fb.comment,
        "message": "Feedback recorded successfully. Thank you for improving detection accuracy."
    }
