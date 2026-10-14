from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Scan, Finding

router = APIRouter()

@router.get("/analytics/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    scans = db.query(Scan).all()
    findings = db.query(Finding).all()

    total_scans = len(scans)
    total_findings = len(findings)
    high_risk_pages_count = sum(1 for s in scans if s.risk_score >= 50.0)
    avg_risk = round(sum(s.risk_score for s in scans) / total_scans, 1) if total_scans > 0 else 0.0

    category_dist = {}
    severity_dist = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    
    for f in findings:
        category_dist[f.category] = category_dist.get(f.category, 0) + 1
        severity_dist[f.severity] = severity_dist.get(f.severity, 0) + 1

    language_dist = {}
    for s in scans:
        lang = s.language or "en"
        language_dist[lang] = language_dist.get(lang, 0) + 1

    recent_scans = [
        {
            "id": s.id,
            "url": s.url or "Pasted Text Analysis",
            "risk_score": s.risk_score,
            "risk_category": s.risk_category,
            "findings_count": s.findings_count,
            "created_at": s.created_at.isoformat() if s.created_at else ""
        }
        for s in db.query(Scan).order_by(Scan.created_at.desc()).limit(5).all()
    ]

    return {
        "total_scans": total_scans,
        "total_findings": total_findings,
        "high_risk_pages_count": high_risk_pages_count,
        "avg_risk_score": avg_risk,
        "category_distribution": category_dist,
        "severity_distribution": severity_dist,
        "language_distribution": language_dist,
        "recent_scans": recent_scans
    }

@router.get("/analytics/trends")
def get_analytics_trends(db: Session = Depends(get_db)):
    scans = db.query(Scan).order_by(Scan.created_at.asc()).all()
    trend_data = [
        {
            "date": s.created_at.strftime("%Y-%m-%d %H:%M") if s.created_at else "Today",
            "risk_score": s.risk_score,
            "findings": s.findings_count,
            "target": s.url or "Text Scan"
        }
        for s in scans
    ]
    return trend_data
