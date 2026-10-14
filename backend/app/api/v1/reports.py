from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Scan
from app.reports.pdf_generator import generate_scan_pdf
from app.reports.csv_generator import generate_scan_csv
from app.reports.json_generator import generate_scan_json

router = APIRouter()

def _get_scan_dict(scan_id: str, db: Session):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail=f"Scan ID '{scan_id}' not found.")
    
    findings_data = [
        {
            "id": f.id,
            "category": f.category,
            "severity": f.severity,
            "confidence": f.confidence,
            "text_snippet": f.text_snippet,
            "dom_selector": f.dom_selector,
            "rationale": f.rationale,
            "consumer_impact": f.consumer_impact,
            "ccpa_clause": f.ccpa_clause,
            "ccpa_category": f.ccpa_category,
            "recommendation": f.recommendation
        }
        for f in scan.findings
    ]

    return {
        "id": scan.id,
        "url": scan.url,
        "scan_type": scan.scan_type,
        "language": scan.language,
        "status": scan.status,
        "risk_score": scan.risk_score,
        "risk_category": scan.risk_category,
        "findings_count": scan.findings_count,
        "fetch_method": getattr(scan, "fetch_method", "http_client"),
        "content_length_analyzed": getattr(scan, "content_length_analyzed", 0),
        "page_title": getattr(scan, "page_title", None),
        "warnings": getattr(scan, "warnings", []),
        "created_at": scan.created_at.isoformat() if scan.created_at else "",
        "findings": findings_data
    }

@router.get("/reports/{scan_id}/pdf")
def export_pdf(scan_id: str, db: Session = Depends(get_db)):
    scan_dict = _get_scan_dict(scan_id, db)
    pdf_bytes = generate_scan_pdf(scan_dict)
    filename = f"DarkPattern_ComplianceReport_{scan_id[:8]}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/reports/{scan_id}/csv")
def export_csv(scan_id: str, db: Session = Depends(get_db)):
    scan_dict = _get_scan_dict(scan_id, db)
    csv_str = generate_scan_csv(scan_dict)
    filename = f"DarkPattern_ComplianceReport_{scan_id[:8]}.csv"
    return Response(
        content=csv_str,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/reports/{scan_id}/json")
def export_json(scan_id: str, db: Session = Depends(get_db)):
    scan_dict = _get_scan_dict(scan_id, db)
    json_str = generate_scan_json(scan_dict)
    filename = f"DarkPattern_ComplianceReport_{scan_id[:8]}.json"
    return Response(
        content=json_str,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
