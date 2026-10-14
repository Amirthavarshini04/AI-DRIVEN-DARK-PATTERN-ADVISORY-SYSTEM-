from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import logging

from app.database.session import get_db
from app.database.models import Scan, Finding
from app.schemas.scan import ScanCreateText, ScanCreateUrl, ScanResponse
from app.core.ssrf import safe_fetch_url, normalize_url, validate_url_security
from app.detection.browser_crawler import is_playwright_available, fetch_page_with_browser
from app.detection.content_extractor import extract_structured_page_content
from app.detection.classifier import analyze_text_content, analyze_structured_elements, detect_language
from app.risk_scoring.combined_risk_model import calculate_combined_risk_score

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/scans/text", response_model=ScanResponse)
def scan_pasted_text(payload: ScanCreateText, db: Session = Depends(get_db)):
    detected_lang = payload.language if payload.language != "auto" else detect_language(payload.text)
    
    # 1. Analyze text for dark pattern findings
    raw_findings = analyze_text_content(payload.text, target_language=detected_lang)
    
    # 2. Compute combined risk score
    risk_score, risk_cat, _, _ = calculate_combined_risk_score(raw_findings)

    # 3. Create Scan DB Record
    scan_obj = Scan(
        url=None,
        scan_type="text",
        language=detected_lang,
        status="completed",
        risk_score=risk_score,
        risk_category=risk_cat,
        findings_count=len(raw_findings),
        fetch_method="text_input",
        content_length_analyzed=len(payload.text),
        page_title="Direct Text Snippet Audit",
        warnings=[],
        raw_text=payload.text[:4000]
    )
    db.add(scan_obj)
    db.flush()

    # 4. Save findings
    for f in raw_findings:
        finding_obj = Finding(
            scan_id=scan_obj.id,
            category=f["category"],
            severity=f["severity"],
            confidence=f["confidence"],
            text_snippet=f["text_snippet"],
            dom_selector=f.get("dom_selector", ".ec-element"),
            rationale=f["rationale"],
            consumer_impact=f["consumer_impact"],
            ccpa_clause=f["ccpa_clause"],
            ccpa_category=f["ccpa_category"],
            recommendation=f["recommendation"]
        )
        db.add(finding_obj)

    db.commit()
    db.refresh(scan_obj)
    return scan_obj

@router.post("/scans/url", response_model=ScanResponse)
def scan_web_url(payload: ScanCreateUrl, db: Session = Depends(get_db)):
    # 1. URL Normalization & SSRF Validation
    normalized_url = normalize_url(payload.url)
    is_safe, sec_msg = validate_url_security(normalized_url)
    if not is_safe:
        raise HTTPException(
            status_code=400,
            detail=f"Target URL Security / Network Failure: {sec_msg}"
        )

    fetch_method = "http_client"
    warnings: List[str] = []
    html_content = ""
    page_title = ""
    browser_elements = []

    # 2. Hybrid Fetch: Try Headless Browser first if available for full JS-rendered DOM
    browser_succeeded = False
    if is_playwright_available():
        b_ok, b_msg, b_title, b_html, b_elems, b_warns = fetch_page_with_browser(
            normalized_url,
            timeout_ms=15000,
            wait_time_ms=1500
        )
        warnings.extend(b_warns)
        if b_ok and b_html and len(b_html.strip()) > 100:
            browser_succeeded = True
            fetch_method = "browser_headless"
            html_content = b_html
            page_title = b_title
            browser_elements = b_elems
        else:
            warnings.append(f"Browser rendering note: {b_msg}. Retrying with HTTP client fallback.")

    # 3. HTTP Client fallback if browser rendering was not used or failed
    if not browser_succeeded:
        http_ok, http_msg, http_html, http_warns = safe_fetch_url(normalized_url, timeout=12)
        warnings.extend(http_warns)
        if not http_ok:
            raise HTTPException(
                status_code=400,
                detail=f"Target URL Retrieval Failure: {http_msg}"
            )
        fetch_method = "http_client"
        html_content = http_html

    # 4. Structured Semantic Content Extraction
    page_data = extract_structured_page_content(html_content, base_url=normalized_url)
    if not page_title and page_data.get("title"):
        page_title = page_data["title"]

    combined_text = page_data.get("combined_text", "")
    content_len = len(combined_text)

    # 5. Assess Content Sufficiency
    if page_data.get("is_empty") or content_len < 30:
        status = "insufficient_content"
        warnings.append(
            "Insufficient readable content extracted from webpage. "
            "The site may enforce strict bot challenges, requires user authentication, or relies on client-side frameworks."
        )
    elif warnings:
        status = "partially_scanned"
    else:
        status = "completed"

    detected_lang = payload.language if payload.language != "auto" else detect_language(combined_text)

    # 6. Multilingual CCPA 2023 Dark Pattern Detection
    # Analyze structured DOM elements (with exact CSS selectors and checkbox states)
    all_elements = list(page_data.get("elements", []))
    if browser_elements:
        for be in browser_elements:
            if not any(e.get("text") == be.get("text") for e in all_elements):
                all_elements.append(be)

    raw_findings = analyze_structured_elements(all_elements, target_language=detected_lang)

    # Also run text classifier on combined text to catch multi-sentence statements
    text_findings = analyze_text_content(combined_text, target_language=detected_lang)
    for tf in text_findings:
        if not any(f["text_snippet"] == tf["text_snippet"] and f["category"] == tf["category"] for f in raw_findings):
            raw_findings.append(tf)

    # 7. Compute Transparent Risk Score
    risk_score, risk_cat, _, _ = calculate_combined_risk_score(raw_findings)

    # 8. Save Scan Record
    scan_obj = Scan(
        url=normalized_url,
        scan_type="url",
        language=detected_lang,
        status=status,
        risk_score=risk_score,
        risk_category=risk_cat,
        findings_count=len(raw_findings),
        fetch_method=fetch_method,
        content_length_analyzed=content_len,
        page_title=page_title or normalized_url,
        warnings=warnings,
        raw_text=combined_text[:4000]
    )
    db.add(scan_obj)
    db.flush()

    for f in raw_findings:
        finding_obj = Finding(
            scan_id=scan_obj.id,
            category=f["category"],
            severity=f["severity"],
            confidence=f["confidence"],
            text_snippet=f["text_snippet"],
            dom_selector=f.get("dom_selector", ".ec-element"),
            rationale=f["rationale"],
            consumer_impact=f["consumer_impact"],
            ccpa_clause=f["ccpa_clause"],
            ccpa_category=f["ccpa_category"],
            recommendation=f["recommendation"]
        )
        db.add(finding_obj)

    db.commit()
    db.refresh(scan_obj)
    return scan_obj

@router.get("/scans")
def list_scans(
    query: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    q = db.query(Scan)
    if query:
        q = q.filter(Scan.url.contains(query) | Scan.raw_text.contains(query))
    total = q.count()
    items = q.order_by(Scan.created_at.desc()).offset(offset).limit(limit).all()
    return {"total": total, "items": items}

@router.get("/scans/{scan_id}", response_model=ScanResponse)
def get_scan(scan_id: str, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail=f"Scan record '{scan_id}' not found.")
    return scan

@router.delete("/scans/{scan_id}")
def delete_scan(scan_id: str, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail=f"Scan record '{scan_id}' not found.")
    db.delete(scan)
    db.commit()
    return {"message": f"Scan '{scan_id}' deleted successfully."}
